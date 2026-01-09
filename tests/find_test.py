import pytest
from pathlib import Path
import tempfile
import shutil
from kuling import find_matching_paths


class TestNonWildcardPaths:
    def test_single_existing_file(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "root1.txt").touch()

        result = find_matching_paths(str(tmp / "root1.txt"))
        assert len(result) == 1
        assert result[0].name == "root1.txt"
        assert result[0].is_file()
        assert result[0].exists()

        shutil.rmtree(tmp)

    def test_nested_existing_file(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "dir1").mkdir()
        (tmp / "dir1" / "file1.txt").touch()

        result = find_matching_paths(str(tmp / "dir1" / "file1.txt"))
        assert len(result) == 1
        assert result[0].name == "file1.txt"
        assert result[0].parent.name == "dir1"
        assert result[0].is_file()

        shutil.rmtree(tmp)

    def test_nonexistent_file_no_raise(self):
        tmp = Path(tempfile.mkdtemp())

        result = find_matching_paths(str(tmp / "nonexistent.txt"))
        assert result == []
        assert isinstance(result, list)
        assert len(result) == 0

        shutil.rmtree(tmp)

    def test_nonexistent_file_with_raise(self):
        tmp = Path(tempfile.mkdtemp())

        with pytest.raises(FileNotFoundError, match="No files found"):
            find_matching_paths(
                str(tmp / "nonexistent.txt"), raise_error_if_no_match=True
            )

        shutil.rmtree(tmp)

    def test_directory_returns_empty(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "empty_dir").mkdir()

        result = find_matching_paths(str(tmp / "empty_dir"))
        assert result == []
        assert isinstance(result, list)

        shutil.rmtree(tmp)

    def test_deeply_nested_file(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "a").mkdir()
        (tmp / "a" / "b").mkdir()
        (tmp / "a" / "b" / "c").mkdir()
        (tmp / "a" / "b" / "c" / "deep.txt").touch()

        result = find_matching_paths(str(tmp / "a" / "b" / "c" / "deep.txt"))
        assert len(result) == 1
        assert result[0].name == "deep.txt"
        assert "a" in result[0].parts
        assert "b" in result[0].parts
        assert "c" in result[0].parts

        shutil.rmtree(tmp)

    def test_file_with_special_characters_in_name(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file-with-dashes.txt").touch()
        (tmp / "file_with_underscores.txt").touch()
        (tmp / "file.multiple.dots.txt").touch()

        result1 = find_matching_paths(str(tmp / "file-with-dashes.txt"))
        result2 = find_matching_paths(str(tmp / "file_with_underscores.txt"))
        result3 = find_matching_paths(str(tmp / "file.multiple.dots.txt"))

        assert len(result1) == 1
        assert len(result2) == 1
        assert len(result3) == 1
        assert result1[0].name == "file-with-dashes.txt"
        assert result2[0].name == "file_with_underscores.txt"
        assert result3[0].name == "file.multiple.dots.txt"

        shutil.rmtree(tmp)


class TestSimpleWildcards:
    def test_asterisk_in_subdirectory(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "dir1").mkdir()
        (tmp / "dir1" / "file1.txt").touch()
        (tmp / "dir1" / "file2.txt").touch()

        result = find_matching_paths(str(tmp / "dir1" / "*.txt"))
        names = {f.name for f in result}
        assert names == {"file1.txt", "file2.txt"}
        assert len(result) == 2
        assert all(f.parent.name == "dir1" for f in result)
        assert all(f.suffix == ".txt" for f in result)

        shutil.rmtree(tmp)

    def test_asterisk_matches_extension(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "logs").mkdir()
        (tmp / "logs" / "2024").mkdir()
        (tmp / "logs" / "2024" / "app.log").touch()
        (tmp / "logs" / "2024" / "error.log").touch()

        result = find_matching_paths(str(tmp / "logs" / "2024" / "*.log"))
        names = {f.name for f in result}
        assert names == {"app.log", "error.log"}
        assert all(f.suffix == ".log" for f in result)
        assert all(f.parent.name == "2024" for f in result)

        shutil.rmtree(tmp)

    def test_asterisk_no_matches_no_raise(self):
        tmp = Path(tempfile.mkdtemp())

        result = find_matching_paths(str(tmp / "*.xyz"))
        assert result == []
        assert isinstance(result, list)

        shutil.rmtree(tmp)

    def test_asterisk_no_matches_with_raise(self):
        tmp = Path(tempfile.mkdtemp())

        with pytest.raises(FileNotFoundError, match="No files found matching pattern"):
            find_matching_paths(str(tmp / "*.xyz"), raise_error_if_no_match=True)

        shutil.rmtree(tmp)

    def test_asterisk_matches_all_files_in_directory(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file1.txt").touch()
        (tmp / "file2.log").touch()
        (tmp / "file3.py").touch()
        (tmp / "subdir").mkdir()

        result = find_matching_paths(str(tmp / "*"))
        assert len(result) == 3
        names = {f.name for f in result}
        assert names == {"file1.txt", "file2.log", "file3.py"}
        assert all(f.is_file() for f in result)

        shutil.rmtree(tmp)

    def test_asterisk_with_prefix(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "test_file1.txt").touch()
        (tmp / "test_file2.txt").touch()
        (tmp / "other_file.txt").touch()

        result = find_matching_paths(str(tmp / "test_*.txt"))
        names = {f.name for f in result}
        assert names == {"test_file1.txt", "test_file2.txt"}
        assert len(result) == 2

        shutil.rmtree(tmp)

    def test_asterisk_with_suffix(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "report_jan.csv").touch()
        (tmp / "report_feb.csv").touch()
        (tmp / "summary_jan.csv").touch()

        result = find_matching_paths(str(tmp / "report_*.csv"))
        names = {f.name for f in result}
        assert names == {"report_jan.csv", "report_feb.csv"}
        assert all(f.name.startswith("report_") for f in result)

        shutil.rmtree(tmp)


class TestQuestionMarkWildcard:
    def test_question_mark_single_char(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "root1.txt").touch()
        (tmp / "root2.txt").touch()

        result = find_matching_paths(str(tmp / "root?.txt"))
        names = {f.name for f in result}
        assert names == {"root1.txt", "root2.txt"}
        assert len(result) == 2
        assert all(len(f.stem) == 5 for f in result)

        shutil.rmtree(tmp)

    def test_question_mark_with_numbers(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "test1.py").touch()
        (tmp / "test2.py").touch()
        (tmp / "test3.py").touch()

        result = find_matching_paths(str(tmp / "test?.py"))
        names = {f.name for f in result}
        assert names == {"test1.py", "test2.py", "test3.py"}
        assert all(f.suffix == ".py" for f in result)

        shutil.rmtree(tmp)

    def test_question_mark_does_not_match_multiple_chars(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file1.txt").touch()
        (tmp / "file12.txt").touch()
        (tmp / "file123.txt").touch()

        result = find_matching_paths(str(tmp / "file?.txt"))
        names = {f.name for f in result}
        assert names == {"file1.txt"}
        assert len(result) == 1

        shutil.rmtree(tmp)

    def test_multiple_question_marks(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "ab.txt").touch()
        (tmp / "cd.txt").touch()
        (tmp / "xyz.txt").touch()

        result = find_matching_paths(str(tmp / "??.txt"))
        names = {f.name for f in result}
        assert names == {"ab.txt", "cd.txt"}
        assert all(len(f.stem) == 2 for f in result)

        shutil.rmtree(tmp)


class TestCharacterSetWildcard:
    def test_character_set_range(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "test1.py").touch()
        (tmp / "test2.py").touch()
        (tmp / "test3.py").touch()

        result = find_matching_paths(str(tmp / "test[12].py"))
        names = {f.name for f in result}
        assert names == {"test1.py", "test2.py"}
        assert len(result) == 2

        shutil.rmtree(tmp)

    def test_character_set_specific(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "root1.txt").touch()
        (tmp / "root2.txt").touch()

        result = find_matching_paths(str(tmp / "root[12].txt"))
        names = {f.name for f in result}
        assert names == {"root1.txt", "root2.txt"}

        shutil.rmtree(tmp)

    def test_character_set_with_letters(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "filea.txt").touch()
        (tmp / "fileb.txt").touch()
        (tmp / "filec.txt").touch()
        (tmp / "filed.txt").touch()

        result = find_matching_paths(str(tmp / "file[abc].txt"))
        names = {f.name for f in result}
        assert names == {"filea.txt", "fileb.txt", "filec.txt"}
        assert len(result) == 3

        shutil.rmtree(tmp)

    def test_character_set_negation(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "test1.py").touch()
        (tmp / "test2.py").touch()
        (tmp / "test3.py").touch()

        result = find_matching_paths(str(tmp / "test[!1].py"))
        names = {f.name for f in result}
        assert names == {"test2.py", "test3.py"}

        shutil.rmtree(tmp)


class TestMultiLevelWildcards:
    def test_wildcard_in_middle(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "logs").mkdir()
        (tmp / "logs" / "2024").mkdir()
        (tmp / "logs" / "2025").mkdir()
        (tmp / "logs" / "2024" / "app.log").touch()
        (tmp / "logs" / "2025" / "app.log").touch()

        result = find_matching_paths(str(tmp / "logs" / "*" / "app.log"))
        names = {f.name for f in result}
        assert names == {"app.log"}
        assert len(result) == 2
        parent_names = {f.parent.name for f in result}
        assert parent_names == {"2024", "2025"}

        shutil.rmtree(tmp)

    def test_multiple_wildcards(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "logs").mkdir()
        (tmp / "logs" / "2024").mkdir()
        (tmp / "logs" / "2024" / "app.log").touch()
        (tmp / "logs" / "2024" / "error.log").touch()

        result = find_matching_paths(str(tmp / "logs" / "*" / "*.log"))
        names = {f.name for f in result}
        assert "app.log" in names
        assert "error.log" in names
        assert all(f.suffix == ".log" for f in result)

        shutil.rmtree(tmp)

    def test_recursive_wildcard(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "deep").mkdir()
        (tmp / "deep" / "level1").mkdir()
        (tmp / "deep" / "level1" / "level2").mkdir()
        (tmp / "deep" / "level1" / "level2" / "nested.txt").touch()

        result = find_matching_paths(str(tmp / "deep" / "**" / "*.txt"))
        names = {f.name for f in result}
        assert "nested.txt" in names
        assert all(f.is_file() for f in result)

        shutil.rmtree(tmp)

    def test_recursive_wildcard_multiple_levels(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "root.txt").touch()
        (tmp / "level1").mkdir()
        (tmp / "level1" / "file1.txt").touch()
        (tmp / "level1" / "level2").mkdir()
        (tmp / "level1" / "level2" / "file2.txt").touch()
        (tmp / "level1" / "level2" / "level3").mkdir()
        (tmp / "level1" / "level2" / "level3" / "file3.txt").touch()

        result = find_matching_paths(str(tmp / "**" / "*.txt"))
        names = {f.name for f in result}
        assert names == {"root.txt", "file1.txt", "file2.txt", "file3.txt"}
        assert len(result) == 4

        shutil.rmtree(tmp)

    def test_wildcard_at_each_level(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "dir1").mkdir()
        (tmp / "dir2").mkdir()
        (tmp / "dir1" / "sub1").mkdir()
        (tmp / "dir1" / "sub2").mkdir()
        (tmp / "dir2" / "sub3").mkdir()
        (tmp / "dir1" / "sub1" / "file1.txt").touch()
        (tmp / "dir1" / "sub2" / "file2.txt").touch()
        (tmp / "dir2" / "sub3" / "file3.txt").touch()

        result = find_matching_paths(str(tmp / "*" / "*" / "*.txt"))
        names = {f.name for f in result}
        assert names == {"file1.txt", "file2.txt", "file3.txt"}
        assert len(result) == 3

        shutil.rmtree(tmp)


class TestErrorHandling:
    def test_nonexistent_base_directory(self):
        tmp = Path(tempfile.mkdtemp())

        with pytest.raises(NotADirectoryError, match="Base directory does not exist"):
            find_matching_paths(str(tmp / "nonexistent" / "*.txt"))

        shutil.rmtree(tmp)

    def test_nested_nonexistent_base_directory(self):
        tmp = Path(tempfile.mkdtemp())

        with pytest.raises(NotADirectoryError, match="Base directory does not exist"):
            find_matching_paths(str(tmp / "a" / "b" / "c" / "*.txt"))

        shutil.rmtree(tmp)

    def test_base_directory_is_file_not_directory(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file.txt").touch()

        with pytest.raises(NotADirectoryError, match="Base path is not a directory"):
            find_matching_paths(str(tmp / "file.txt" / "*.txt"))

        shutil.rmtree(tmp)

    def test_partial_path_exists(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "existing").mkdir()

        with pytest.raises(NotADirectoryError, match="Base directory does not exist"):
            find_matching_paths(str(tmp / "existing" / "missing" / "*.txt"))

        shutil.rmtree(tmp)


class TestReturnTypes:
    def test_always_returns_list(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file.txt").touch()

        result = find_matching_paths(str(tmp / "*.txt"))
        assert isinstance(result, list)
        assert len(result) > 0

        shutil.rmtree(tmp)

    def test_empty_list_on_no_match(self):
        tmp = Path(tempfile.mkdtemp())

        result = find_matching_paths(str(tmp / "*.nonexistent"))
        assert result == []
        assert isinstance(result, list)
        assert len(result) == 0

        shutil.rmtree(tmp)

    def test_list_contains_path_objects(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file.txt").touch()

        result = find_matching_paths(str(tmp / "*.txt"))
        for item in result:
            assert isinstance(item, Path)
            assert hasattr(item, "name")
            assert hasattr(item, "parent")
            assert hasattr(item, "suffix")

        shutil.rmtree(tmp)

    def test_paths_are_absolute(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file.txt").touch()

        result = find_matching_paths(str(tmp / "*.txt"))
        for item in result:
            assert item.is_absolute()

        shutil.rmtree(tmp)


class TestRaiseErrorFlag:
    def test_raise_false_returns_empty_on_no_match(self):
        tmp = Path(tempfile.mkdtemp())

        result = find_matching_paths(str(tmp / "*.xyz"), raise_error_if_no_match=False)
        assert result == []
        assert isinstance(result, list)

        shutil.rmtree(tmp)

    def test_raise_true_throws_on_no_match(self):
        tmp = Path(tempfile.mkdtemp())

        with pytest.raises(FileNotFoundError):
            find_matching_paths(str(tmp / "*.xyz"), raise_error_if_no_match=True)

        shutil.rmtree(tmp)

    def test_raise_true_no_error_on_match(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "file.txt").touch()

        result = find_matching_paths(str(tmp / "*.txt"), raise_error_if_no_match=True)
        assert len(result) > 0
        assert isinstance(result, list)

        shutil.rmtree(tmp)

    def test_raise_false_is_default(self):
        tmp = Path(tempfile.mkdtemp())

        result1 = find_matching_paths(str(tmp / "*.xyz"))
        result2 = find_matching_paths(str(tmp / "*.xyz"), raise_error_if_no_match=False)
        assert result1 == result2 == []

        shutil.rmtree(tmp)

    def test_raise_true_with_nonexistent_file_no_wildcard(self):
        tmp = Path(tempfile.mkdtemp())

        with pytest.raises(FileNotFoundError):
            find_matching_paths(str(tmp / "missing.txt"), raise_error_if_no_match=True)

        shutil.rmtree(tmp)


class TestComplexPatterns:
    def test_combined_wildcards(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "dir1").mkdir()
        (tmp / "dir2").mkdir()
        (tmp / "dir1" / "file1.txt").touch()
        (tmp / "dir1" / "file2.txt").touch()
        (tmp / "dir2" / "file3.txt").touch()

        result = find_matching_paths(str(tmp / "dir?" / "file?.txt"))
        names = {f.name for f in result}
        expected = {"file1.txt", "file2.txt", "file3.txt"}
        assert names == expected
        assert all(f.suffix == ".txt" for f in result)

        shutil.rmtree(tmp)

    def test_deep_nesting_with_recursive(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "a.txt").touch()
        (tmp / "dir1").mkdir()
        (tmp / "dir1" / "b.txt").touch()
        (tmp / "dir1" / "sub").mkdir()
        (tmp / "dir1" / "sub" / "c.txt").touch()

        result = find_matching_paths(str(tmp / "**" / "*.txt"))
        assert len(result) >= 3
        names = {f.name for f in result}
        assert "a.txt" in names
        assert "b.txt" in names
        assert "c.txt" in names

        shutil.rmtree(tmp)

    def test_asterisk_and_character_set_combination(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "test1_report.csv").touch()
        (tmp / "test2_report.csv").touch()
        (tmp / "test3_summary.csv").touch()

        result = find_matching_paths(str(tmp / "test[12]_*.csv"))
        names = {f.name for f in result}
        assert names == {"test1_report.csv", "test2_report.csv"}

        shutil.rmtree(tmp)

    def test_question_mark_and_asterisk_combination(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "v1_data.txt").touch()
        (tmp / "v2_data.txt").touch()
        (tmp / "v10_data.txt").touch()

        result = find_matching_paths(str(tmp / "v?_*.txt"))
        names = {f.name for f in result}
        assert names == {"v1_data.txt", "v2_data.txt"}
        assert len(result) == 2

        shutil.rmtree(tmp)

    def test_extension_wildcard(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "document.txt").touch()
        (tmp / "document.pdf").touch()
        (tmp / "document.docx").touch()

        result = find_matching_paths(str(tmp / "document.*"))
        assert len(result) == 3
        names = {f.name for f in result}
        assert names == {"document.txt", "document.pdf", "document.docx"}

        shutil.rmtree(tmp)
