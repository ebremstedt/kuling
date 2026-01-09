from pathlib import Path


def delete_file(path: str | Path) -> None:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise IsADirectoryError(f"Path is not a file: {path}")

    path.unlink()
