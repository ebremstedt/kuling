# 💨 Kuling 💨

A simple, intuitive Python library for file operations with clean APIs and robust error handling.

## 🚀 Features

- **Glob Pattern Matching** 🔍 - Find files with support for `*`, `?`, `[abc]`, and `**` wildcards
- **Safe File Operations** 📁 - Move, copy, and delete files with automatic directory creation
- **Robust Error Handling** ⚠️ - Clear exceptions for all edge cases
- **Path Flexibility** 🛤️ - Works with both strings and Path objects
- **Type Safety** 🔒 - Full type hints for better IDE support

## 📦 Installation
```bash
pip install kuling
```

## 🔧 Quick Start
```python
from kuling import find_matching_paths, move_file, copy_file, delete_file

# Find all Python files recursively
python_files = find_matching_paths("/project/**/*.py")

# Move a file (creates parent directories automatically)
move_file("old/location/file.txt", "new/location/file.txt")

# Copy a file to a directory (keeps original name)
copy_file("important.txt", "backups/")

# Delete a file
delete_file("temp/unwanted.log")
```
## 🔧 Advanced Features

### Pattern Matching Examples
```python
# Question mark - single character
find_matching_paths("file?.txt")  # file1.txt, fileA.txt

# Character sets
find_matching_paths("test[123].py")  # test1.py, test2.py, test3.py
find_matching_paths("file[abc].txt")  # filea.txt, fileb.txt, filec.txt

# Negation
find_matching_paths("test[!1].py")  # test2.py, test3.py (not test1.py)

# Recursive search
find_matching_paths("**/*.py")  # All .py files in all subdirectories

# Combined wildcards
find_matching_paths("logs/*/2024/*.log")  # Logs in any subdirectory for 2024
```

### Path Flexibility
```python
from pathlib import Path

# All functions accept both strings and Path objects
source = Path("file.txt")
dest = "backup/"

copy_file(source, dest)  # Mixed types work fine
copy_file(str(source), str(dest))  # Strings work
copy_file(source, Path(dest))  # Path objects work
```

## 🔗 Links

- [Homepage](https://github.com/ebremstedt/kuling)
- [Issues](https://github.com/ebremstedt/kuling/issues)
- [PyPI](https://pypi.org/project/kuling/)
