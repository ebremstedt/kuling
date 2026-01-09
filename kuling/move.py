from pathlib import Path
import shutil


def move_file(source: str | Path, destination: str | Path) -> Path:
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")

    if destination.is_dir():
        destination = destination / source.name

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(src=source, dst=destination)

    return destination
