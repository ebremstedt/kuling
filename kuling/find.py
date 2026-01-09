from pathlib import Path

WILDCARD_CHARS = {"*", "?", "["}


def find_matching_paths(
    path_pattern: str, raise_error_if_no_match: bool = False
) -> list[Path]:
    try:
        path = Path(path_pattern)
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid path pattern '{path_pattern}': {e}") from e

    wildcard_positions = [
        i for i, part in enumerate(path.parts) if any(c in part for c in WILDCARD_CHARS)
    ]

    if not wildcard_positions:
        matches = [path] if path.is_file() else []

        if raise_error_if_no_match and not matches:
            raise FileNotFoundError(f"No files found: {path_pattern}")

        return matches

    first_wildcard_position = wildcard_positions[0]

    base_dir = (
        Path(*path.parts[:first_wildcard_position])
        if first_wildcard_position > 0
        else Path(".")
    )

    if not base_dir.exists():
        raise NotADirectoryError(f"Base directory does not exist: {base_dir}")

    if not base_dir.is_dir():
        raise NotADirectoryError(f"Base path is not a directory: {base_dir}")

    pattern = str(Path(*path.parts[first_wildcard_position:]))
    matches = [f for f in base_dir.glob(pattern) if f.is_file()]

    if raise_error_if_no_match and not matches:
        raise FileNotFoundError(f"No files found matching pattern: {path_pattern}")

    return matches


def move_file(
    source: str | Path,
    destination: str | Path,
    delete_original: bool = False,
) -> Path:
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")

    if destination.is_dir():
        destination = destination / source.name

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src=source, dst=destination)

    if delete_original:
        source.unlink()

    return destination


def delete_file(path: str | Path) -> bool:
    path = Path(path)

    if path.exists():
        path.unlink()
        return True

    return False
