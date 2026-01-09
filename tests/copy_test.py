import pytest
from pathlib import Path
import tempfile
import shutil
from kuling import copy_file


class TestCopyFileBasic:
    def test_copy_file_to_new_location(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("test content")
        destination = tmp / "dest.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert destination.read_text() == "test content"
        assert source.exists()
        assert source.read_text() == "test content"

        shutil.rmtree(tmp)

    def test_copy_file_to_existing_directory(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        dest_dir = tmp / "target_dir"
        dest_dir.mkdir()

        result = copy_file(source, dest_dir)

        assert result == dest_dir / "file.txt"
        assert (dest_dir / "file.txt").exists()
        assert (dest_dir / "file.txt").read_text() == "content"
        assert source.exists()

        shutil.rmtree(tmp)

    def test_copy_file_with_different_name(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "old_name.txt"
        source.write_text("data")
        destination = tmp / "new_name.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert destination.name == "new_name.txt"
        assert source.exists()
        assert source.name == "old_name.txt"

        shutil.rmtree(tmp)

    def test_copy_preserves_file_content(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "data.txt"
        content = "important data\nline 2\nline 3"
        source.write_text(content)
        destination = tmp / "copied.txt"

        copy_file(source, destination)

        assert destination.read_text() == content
        assert source.read_text() == content

        shutil.rmtree(tmp)

    def test_copy_leaves_source_unchanged(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("original")
        destination = tmp / "dest.txt"

        copy_file(source, destination)

        assert source.exists()
        assert source.read_text() == "original"
        assert destination.exists()
        assert destination.read_text() == "original"

        shutil.rmtree(tmp)


class TestCopyFileWithNonexistentPaths:
    def test_copy_to_nonexistent_directory(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "new_dir" / "file.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert (tmp / "new_dir").exists()
        assert (tmp / "new_dir").is_dir()
        assert source.exists()

        shutil.rmtree(tmp)

    def test_copy_to_deeply_nested_nonexistent_path(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "a" / "b" / "c" / "d" / "file.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert (tmp / "a" / "b" / "c" / "d").exists()
        assert source.exists()

        shutil.rmtree(tmp)

    def test_source_file_not_found(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "nonexistent.txt"
        destination = tmp / "dest.txt"

        with pytest.raises(FileNotFoundError, match="File not found"):
            copy_file(source, destination)

        shutil.rmtree(tmp)


class TestCopyFileEdgeCases:
    def test_copy_empty_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "empty.txt"
        source.touch()
        destination = tmp / "copied_empty.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert destination.stat().st_size == 0
        assert source.exists()

        shutil.rmtree(tmp)

    def test_copy_large_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "large.txt"
        large_content = "x" * 10000
        source.write_text(large_content)
        destination = tmp / "copied_large.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.read_text() == large_content
        assert source.read_text() == large_content

        shutil.rmtree(tmp)

    def test_copy_file_with_special_characters_in_name(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file-with_special.chars.txt"
        source.write_text("content")
        destination = tmp / "new-file_special.chars.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert source.exists()

        shutil.rmtree(tmp)

    def test_copy_binary_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "binary.dat"
        binary_data = bytes([0, 1, 2, 255, 254, 253])
        source.write_bytes(binary_data)
        destination = tmp / "copied_binary.dat"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.read_bytes() == binary_data
        assert source.read_bytes() == binary_data

        shutil.rmtree(tmp)


class TestCopyFileWithPathTypes:
    def test_copy_with_string_paths(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "dest.txt"

        result = copy_file(str(source), str(destination))

        assert result == destination
        assert destination.exists()
        assert source.exists()

        shutil.rmtree(tmp)

    def test_copy_with_path_objects(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "dest.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert source.exists()

        shutil.rmtree(tmp)

    def test_copy_with_mixed_path_types(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "dest.txt"

        result = copy_file(str(source), destination)

        assert result == destination
        assert destination.exists()
        assert source.exists()

        shutil.rmtree(tmp)


class TestCopyFileReturnValue:
    def test_returns_path_object(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "dest.txt"

        result = copy_file(source, destination)

        assert isinstance(result, Path)
        assert result == destination

        shutil.rmtree(tmp)

    def test_returns_correct_path_when_copying_to_directory(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "myfile.txt"
        source.write_text("content")
        dest_dir = tmp / "target"
        dest_dir.mkdir()

        result = copy_file(source, dest_dir)

        assert result == dest_dir / "myfile.txt"
        assert result.name == "myfile.txt"

        shutil.rmtree(tmp)


class TestCopyFileOverwriting:
    def test_copy_overwrites_existing_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("new content")
        destination = tmp / "dest.txt"
        destination.write_text("old content")

        result = copy_file(source, destination)

        assert result == destination
        assert destination.read_text() == "new content"
        assert source.exists()
        assert source.read_text() == "new content"

        shutil.rmtree(tmp)

    def test_copy_to_directory_with_existing_file(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("new content")
        dest_dir = tmp / "target"
        dest_dir.mkdir()
        (dest_dir / "file.txt").write_text("old content")

        result = copy_file(source, dest_dir)

        assert result == dest_dir / "file.txt"
        assert (dest_dir / "file.txt").read_text() == "new content"
        assert source.exists()

        shutil.rmtree(tmp)


class TestCopyFileCrossPaths:
    def test_copy_from_nested_to_root(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "nested" / "deep").mkdir(parents=True)
        source = tmp / "nested" / "deep" / "file.txt"
        source.write_text("content")
        destination = tmp / "copied.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert source.exists()

        shutil.rmtree(tmp)

    def test_copy_from_root_to_nested(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "file.txt"
        source.write_text("content")
        destination = tmp / "new" / "nested" / "path" / "file.txt"

        result = copy_file(source, destination)

        assert result == destination
        assert destination.exists()
        assert source.exists()

        shutil.rmtree(tmp)


class TestCopyFileMultipleCopies:
    def test_copy_same_file_multiple_times(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("content")
        dest1 = tmp / "copy1.txt"
        dest2 = tmp / "copy2.txt"
        dest3 = tmp / "copy3.txt"

        copy_file(source, dest1)
        copy_file(source, dest2)
        copy_file(source, dest3)

        assert source.exists()
        assert dest1.exists()
        assert dest2.exists()
        assert dest3.exists()
        assert dest1.read_text() == "content"
        assert dest2.read_text() == "content"
        assert dest3.read_text() == "content"

        shutil.rmtree(tmp)

    def test_copy_to_multiple_directories(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("content")
        (tmp / "dir1").mkdir()
        (tmp / "dir2").mkdir()
        (tmp / "dir3").mkdir()

        copy_file(source, tmp / "dir1")
        copy_file(source, tmp / "dir2")
        copy_file(source, tmp / "dir3")

        assert source.exists()
        assert (tmp / "dir1" / "source.txt").exists()
        assert (tmp / "dir2" / "source.txt").exists()
        assert (tmp / "dir3" / "source.txt").exists()

        shutil.rmtree(tmp)


class TestCopyFileIndependence:
    def test_modifying_copy_does_not_affect_source(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("original")
        destination = tmp / "copy.txt"

        copy_file(source, destination)
        destination.write_text("modified")

        assert source.read_text() == "original"
        assert destination.read_text() == "modified"

        shutil.rmtree(tmp)

    def test_modifying_source_does_not_affect_copy(self):
        tmp = Path(tempfile.mkdtemp())
        source = tmp / "source.txt"
        source.write_text("original")
        destination = tmp / "copy.txt"

        copy_file(source, destination)
        source.write_text("modified")

        assert source.read_text() == "modified"
        assert destination.read_text() == "original"

        shutil.rmtree(tmp)
