from pathlib import Path
import tempfile
from kuling.find import find_matching_paths
import shutil

# Create test directory structure
test_dir = Path(tempfile.mkdtemp())
(test_dir / "logs").mkdir()
(test_dir / "logs/2024").mkdir()
(test_dir / "data").mkdir()
(test_dir / "data/jan").mkdir()
(test_dir / "data/feb").mkdir()

# Create test files
(test_dir / "file1.txt").touch()
(test_dir / "file2.txt").touch()
(test_dir / "logs/2024/app.log").touch()
(test_dir / "logs/2024/error.log").touch()
(test_dir / "data/jan/report.csv").touch()
(test_dir / "data/feb/report.csv").touch()

# Run examples
print(f"Test directory: {test_dir}\n")

print("Example 1: *.txt")
result = find_matching_paths(str(test_dir / "*.txt"))
print(f"Found: {[f.name for f in result]}\n")

print("Example 2: logs/2024/*.log")
result = find_matching_paths(str(test_dir / "logs/2024/*.log"))
print(f"Found: {[f.name for f in result]}\n")

print("Example 3: data/*/report.csv")
result = find_matching_paths(str(test_dir / "data/*/report.csv"))
print(f"Found: {[f.relative_to(test_dir) for f in result]}\n")

print("Example 4: No wildcards - existing file")
result = find_matching_paths(str(test_dir / "file1.txt"))
print(f"Found: {[f.name for f in result]}\n")

print("Example 5: */report.csv")
result = find_matching_paths(str(test_dir / "data/*/report.csv"))
print(f"Found: {[f.relative_to(test_dir) for f in result]}\n")

# Cleanup
shutil.rmtree(test_dir)
