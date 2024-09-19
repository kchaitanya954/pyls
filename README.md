# PyLS - Python LS Implementation

PyLS is a Python implementation of the Unix `ls` command, designed to work with a JSON representation of a directory structure.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/kchaitanya954/pyls.git
   cd pyls
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode:
   ```
   pip install -e .
   ```

## Usage

After installation, you can use the `pyls` command:

```
pyls [options] [path]
```

Options:
- `-a`, `--all`: Do not ignore entries starting with .
- `-l`: Use a long listing format
- `-r`, `--reverse`: Reverse order while sorting
- `-t`: Sort by modification time, newest first
- `--filter {file,dir}`: Filter output (file or dir)
- `-H`, `--human-readable`: Show human-readable file sizes

## Development

To set up the development environment:

1. Install development dependencies:
   ```
   pip install -e .[dev]
   ```

2. Run tests:
   ```
   pytest
   ```

3. Check code style:
   ```
   flake8 src/pyls.py
   ```

## Project Structure

```
pyls/
│
├── src/
│   └── pyls.py
│
├── tests/
│   └── test_pyls.py
│
├── pyproject.toml
├── README.md
└── .gitignore
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.