from pathlib import Path
import shutil


def copy_file(source: str | Path, destination: str | Path) -> Path:
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileNotFoundError(f"File not found: {source}")

    if destination.is_dir():
        destination = destination / source.name

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src=source, dst=destination)

    return destination
