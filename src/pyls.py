#!/usr/bin/env python3

import json
import sys
import argparse
from datetime import datetime
import os
from typing import Dict, List, Union, Optional

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Python implementation of ls command')
    parser.add_argument('path', nargs='?', default='.', help='Path to list contents of')
    parser.add_argument('-a', '--all', action='store_true', help='Do not ignore entries starting with .')
    parser.add_argument('-l', action='store_true', help='Use a long listing format')
    parser.add_argument('-r', '--reverse', action='store_true', help='Reverse order while sorting')
    parser.add_argument('-t', action='store_true', help='Sort by modification time, newest first')
    parser.add_argument('--filter', choices=['file', 'dir'], help='Filter output (file or dir)')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Show human-readable file sizes')
    return parser.parse_args()

def load_json(file_path: str = 'structure.json') -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)

def format_permissions(permissions: str) -> str:
    return permissions

def format_time(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%b %d %H:%M')

def format_size(size: int, human_readable: bool = False) -> str:
    if not human_readable or size < 1024:
        return f"{size:8d}"
    
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(size) < 1024.0:
            return f"{size:3.1f}{unit}".rjust(8)
        size /= 1024.0
    return f"{size:.1f}Y".rjust(8)

def is_directory(item: Dict) -> bool:
    return 'contents' in item

def find_item(data: Dict, path: str) -> Dict:
    parts = path.strip('./').split('/')
    current = data
    for part in parts:
        if part == '':
            continue
        if is_directory(current):
            current = next((item for item in current['contents'] if item['name'] == part), None)
            if current is None:
                raise FileNotFoundError(f"Cannot access '{path}': No such file or directory")
        else:
            raise FileNotFoundError(f"Cannot access '{path}': Not a directory")
    return current

def list_contents(item: Dict, show_all: bool = False, long_format: bool = False, 
                  reverse: bool = False, sort_by_time: bool = False, 
                  filter_type: Optional[str] = None, human_readable: bool = False) -> None:
    if not is_directory(item):
        print_item(item, long_format, human_readable)
        return

    contents = item.get('contents', [])
    
    if sort_by_time:
        contents.sort(key=lambda x: x['time_modified'], reverse=not reverse)
    else:
        contents.sort(key=lambda x: x['name'].lower(), reverse=reverse)
    
    for content_item in contents:
        name = content_item['name']
        if not show_all and name.startswith('.'):
            continue
        
        if filter_type == 'file' and is_directory(content_item):
            continue
        if filter_type == 'dir' and not is_directory(content_item):
            continue
        
        print_item(content_item, long_format, human_readable)

def print_item(item: Dict, long_format: bool, human_readable: bool) -> None:
    name = item['name']
    if long_format:
        permissions = format_permissions(item['permissions'])
        size = format_size(item['size'], human_readable)
        time = format_time(item['time_modified'])
        print(f"{permissions} {size} {time} {name}")
    else:
        print(name)

def main() -> None:
    args = parse_args()
    data = load_json()
    
    try:
        item = find_item(data, args.path)
        list_contents(item, 
                      show_all=args.all, 
                      long_format=args.l, 
                      reverse=args.reverse, 
                      sort_by_time=args.t, 
                      filter_type=args.filter,
                      human_readable=args.human_readable)
    except FileNotFoundError as e:
        print(f"error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()