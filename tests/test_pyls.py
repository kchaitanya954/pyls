import pytest
from src.pyls import format_size, is_directory, find_item

def test_format_size():
    assert format_size(1000) == "    1000"
    assert format_size(1024, human_readable=True) == "   1.0K"
    assert format_size(1048576, human_readable=True) == "   1.0M"

def test_is_directory():
    assert is_directory({"contents": []}) == True
    assert is_directory({"name": "file.txt"}) == False

def test_find_item():
    data = {
        "name": "root",
        "contents": [
            {"name": "file1.txt"},
            {"name": "dir1", "contents": [{"name": "file2.txt"}]}
        ]
    }
    assert find_item(data, "file1.txt")["name"] == "file1.txt"
    assert find_item(data, "dir1/file2.txt")["name"] == "file2.txt"
    with pytest.raises(FileNotFoundError):
        find_item(data, "nonexistent")

# Add more tests as needed