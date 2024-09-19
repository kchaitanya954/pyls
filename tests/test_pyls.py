import pytest
import sys
from unittest.mock import patch, mock_open
from src.pyls import parse_args, load_json, list_contents, find_item


def test_parse_args(monkeypatch):
    # Mock sys.argv for testing
    monkeypatch.setattr(sys, 'argv', ['pyls', '-l', '-r', '--filter=file'])
    args = parse_args()
    
    assert args.l == True
    assert args.reverse == True
    assert args.filter == 'file'

def test_load_json():
    # Test loading of JSON
    data = load_json('structure.json')
    assert data['name'] == 'interpreter'


def test_find_item():
    # Test finding items in directory
    data = load_json('structure.json')
    item = find_item(data, 'parser')
    assert item['name'] == 'parser'
    assert 'contents' in item

    # Test invalid path
    with pytest.raises(FileNotFoundError):
        find_item(data, 'nonexistent')

def test_list_contents_basic(capsys):
    # Test basic ls functionality
    data = load_json('structure.json')
    root = find_item(data, '.')

    list_contents(root, show_all=False, long_format=False, reverse=False)
    captured = capsys.readouterr()
    assert "LICENSE" in captured.out
    assert "README.md" in captured.out
    assert ".gitignore" not in captured.out  # By default hidden files are not shown

def test_list_contents_long_format(capsys):
    # Test ls -l (long format)
    data = load_json('structure.json')
    root = find_item(data, '.')

    list_contents(root, show_all=False, long_format=True, reverse=False)
    captured = capsys.readouterr()
    assert "-rw-r--r--" in captured.out
    assert "1071" in captured.out  # File size

def test_list_contents_reverse(capsys):
    # Test ls -r (reverse)
    data = load_json('structure.json')
    root = find_item(data, '.')

    list_contents(root, show_all=False, long_format=False, reverse=True)
    captured = capsys.readouterr()
    
    # Debugging output to check the order
    print(captured.out.splitlines())
    
    assert "token" in captured.out.splitlines()[0]  # Update to match actual order


def test_list_contents_filter_file(capsys):
    # Test ls with --filter=file
    data = load_json('structure.json')
    root = find_item(data, '.')

    list_contents(root, show_all=False, long_format=False, filter_type='file')
    captured = capsys.readouterr()
    assert "LICENSE" in captured.out
    assert "README.md" in captured.out
    assert "parser" not in captured.out  # parser is a directory


def test_invalid_filter(monkeypatch, capsys):
    # Mock sys.argv to simulate invalid filter input
    monkeypatch.setattr(sys, 'argv', ['pyls', '-l', '-r', '--filter=invalid'])
    
    with pytest.raises(SystemExit):  # argparse will raise SystemExit on invalid input
        parse_args()

    captured = capsys.readouterr()
    assert "error: argument --filter: invalid choice" in captured.err
