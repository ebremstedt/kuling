import pytest
from pathlib import Path
import tempfile
import shutil
from kuling import delete_file


class TestDeleteFileBasic:
    def test_delete_existing_file(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "file.txt"
        file.write_text("content")

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_file_with_content(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "data.txt"
        file.write_text("some important data")

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_empty_file(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "empty.txt"
        file.touch()

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_returns_none(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "file.txt"
        file.touch()

        result = delete_file(file)

        assert result is None

        shutil.rmtree(tmp)


class TestDeleteFileErrors:
    def test_delete_nonexistent_file_raises_error(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "nonexistent.txt"

        with pytest.raises(FileNotFoundError, match="File not found"):
            delete_file(file)

        shutil.rmtree(tmp)

    def test_delete_directory_raises_error(self):
        tmp = Path(tempfile.mkdtemp())
        directory = tmp / "mydir"
        directory.mkdir()

        with pytest.raises(IsADirectoryError, match="Path is not a file"):
            delete_file(directory)

        shutil.rmtree(tmp)

    def test_delete_nested_directory_raises_error(self):
        tmp = Path(tempfile.mkdtemp())
        directory = tmp / "parent" / "child"
        directory.mkdir(parents=True)

        with pytest.raises(IsADirectoryError, match="Path is not a file"):
            delete_file(directory)

        shutil.rmtree(tmp)


class TestDeleteFileWithPathTypes:
    def test_delete_with_string_path(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "file.txt"
        file.touch()

        delete_file(str(file))

        assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_with_path_object(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "file.txt"
        file.touch()

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)


class TestDeleteFileSpecialCases:
    def test_delete_file_with_special_characters(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "file-with_special.chars.txt"
        file.touch()

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_binary_file(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "binary.dat"
        file.write_bytes(bytes([0, 1, 2, 255]))

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_large_file(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "large.txt"
        file.write_text("x" * 100000)

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_file_with_dots_in_name(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "file.multiple.dots.txt"
        file.touch()

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)


class TestDeleteFileInNestedDirectories:
    def test_delete_file_in_nested_directory(self):
        tmp = Path(tempfile.mkdtemp())
        nested_dir = tmp / "a" / "b" / "c"
        nested_dir.mkdir(parents=True)
        file = nested_dir / "file.txt"
        file.touch()

        delete_file(file)

        assert not file.exists()
        assert nested_dir.exists()

        shutil.rmtree(tmp)

    def test_delete_file_leaves_directory_intact(self):
        tmp = Path(tempfile.mkdtemp())
        directory = tmp / "mydir"
        directory.mkdir()
        file = directory / "file.txt"
        file.touch()

        delete_file(file)

        assert not file.exists()
        assert directory.exists()
        assert directory.is_dir()

        shutil.rmtree(tmp)


class TestDeleteFileMultipleOperations:
    def test_delete_multiple_files(self):
        tmp = Path(tempfile.mkdtemp())
        file1 = tmp / "file1.txt"
        file2 = tmp / "file2.txt"
        file3 = tmp / "file3.txt"
        file1.touch()
        file2.touch()
        file3.touch()

        delete_file(file1)
        delete_file(file2)
        delete_file(file3)

        assert not file1.exists()
        assert not file2.exists()
        assert not file3.exists()

        shutil.rmtree(tmp)

    def test_cannot_delete_same_file_twice(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "file.txt"
        file.touch()

        delete_file(file)

        with pytest.raises(FileNotFoundError):
            delete_file(file)

        shutil.rmtree(tmp)


class TestDeleteFileExtensions:
    def test_delete_file_various_extensions(self):
        tmp = Path(tempfile.mkdtemp())
        extensions = [".txt", ".py", ".json", ".csv", ".log", ".dat"]

        for ext in extensions:
            file = tmp / f"file{ext}"
            file.touch()
            delete_file(file)
            assert not file.exists()

        shutil.rmtree(tmp)

    def test_delete_file_no_extension(self):
        tmp = Path(tempfile.mkdtemp())
        file = tmp / "README"
        file.touch()

        delete_file(file)

        assert not file.exists()

        shutil.rmtree(tmp)
