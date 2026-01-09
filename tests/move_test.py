import pytest
from pathlib import Path
import tempfile
import shutil
from kuling import move_file


class TestMoveFileBasic:
    def test_move_file_to_new_location(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("test content")
        destination = tmp / "dest.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert destination.read_text() == "test content"
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_file_to_existing_directory(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        dest_dir = tmp / "target_dir"
        dest_dir.mkdir()

        result = move_file(source, dest_dir)

        assert result == dest_dir / "file.txt"
        assert (dest_dir / "file.txt").exists()
        assert (dest_dir / "file.txt").read_text() == "content"
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_file_with_different_name(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "old_name.txt"
        source.write_text("data")
        destination = tmp / "new_name.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert destination.name == "new_name.txt"
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_preserves_file_content(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "data.txt"
        content = "important data\nline 2\nline 3"
        source.write_text(content)
        destination = tmp / "moved.txt"

        move_file(source, destination)

        assert destination.read_text() == content

        shutil.rmtree(tmp)


class TestMoveFileWithNonexistentPaths:
    def test_move_to_nonexistent_directory(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "new_dir" / "file.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert (tmp / "new_dir").exists()
        assert (tmp / "new_dir").is_dir()
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_to_deeply_nested_nonexistent_path(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "a" / "b" / "c" / "d" / "file.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert (tmp / "a" / "b" / "c" / "d").exists()
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_source_file_not_found(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "nonexistent.txt"
        destination = tmp / "dest.txt"

        with pytest.raises(FileNotFoundError, match="File not found"):
            move_file(source, destination)

        shutil.rmtree(tmp)


class TestMoveFileEdgeCases:
    def test_move_empty_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "empty.txt"
        source.touch()
        destination = tmp / "moved_empty.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert destination.stat().st_size == 0
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_large_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "large.txt"
        large_content = "x" * 10000
        source.write_text(large_content)
        destination = tmp / "moved_large.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.read_text() == large_content
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_file_with_special_characters_in_name(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file-with_special.chars.txt"
        source.write_text("content")
        destination = tmp / "new-file_special.chars.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_binary_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "binary.dat"
        binary_data = bytes([0, 1, 2, 255, 254, 253])
        source.write_bytes(binary_data)
        destination = tmp / "moved_binary.dat"

        result = move_file(source, destination)

        assert result == destination
        assert destination.read_bytes() == binary_data
        assert not source.exists()

        shutil.rmtree(tmp)


class TestMoveFileWithPathTypes:
    def test_move_with_string_paths(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "dest.txt"

        result = move_file(str(source), str(destination))

        assert result == destination
        assert destination.exists()
        assert not source.exists()

        shutil.rmtree(tmp)

    def test_move_with_path_objects(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "dest.txt"

        result = move_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert not source.exists()

        shutil.rmtree(tmp)
