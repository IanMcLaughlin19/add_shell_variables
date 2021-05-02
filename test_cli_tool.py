import sys
from cli import create_parse, main
import unittest
import filecmp
import os
import pathlib


class TestCLI(unittest.TestCase):
    """
    Tests all the basic functionality of the CLI.
    """

    @staticmethod
    def two_text_files_equal( file_path_1: str, file_path_2: str) -> bool:
        """
        Helper that checks whether two files are equal
        :param file_path_1: path to first file
        :param file_path_2: path to second file
        :return: bool true if files are equal else false
        """
        return filecmp.cmp(file_path_1, file_path_2)


    def setUp(self) -> None:
        """
        Sets a clean parser for each unnitest
        """
        self.parser = create_parse()
        self.project_directory = str(pathlib.Path(__file__).parent.absolute())
        path_to_test_files_dir = self.project_directory + "\\test\\test_files\\"
        test_files = os.listdir(path_to_test_files_dir)
        full_paths_test_files = []
        for file in test_files:
            full_path = path_to_test_files_dir + file
            full_paths_test_files.append(full_path)
        self.file_copy_dict = {}
        for file_path in full_paths_test_files:
            self.file_copy_dict[file_path] = open(file_path, 'r').readlines()

    def tearDown(self) -> None:
        """
        Restores all the files in test_files
        """
        for file, file_lines in self.file_copy_dict.items():
            with open(file, 'w') as f:
                f.writelines(file_lines)
                f.close()

    def test_add_var(self):
        path_to_test_bashrc_original = self.project_directory + "\\test\\test_files\\test_blank_bash_file.sh"
        path_to_test_bashrc_altered = self.project_directory + "\\test\\test_files\\test_blank_bash_file_one_var.sh"
        self.assertFalse(self.two_text_files_equal(path_to_test_bashrc_original, path_to_test_bashrc_altered))
        args = self.parser.parse_args(["-k", "TEST_VAR", "-v", "test", "-p", path_to_test_bashrc_original])
        main(args)
        altered_lines = open(path_to_test_bashrc_original, 'r').readlines()
        expected_line = "export TEST_VAR=test\n"
        actual_line = altered_lines[2]
        self.assertEqual(expected_line, actual_line)

    def test_add_var_lower_case(self):
        path_to_test_bashrc_original = self.project_directory + "\\test\\test_files\\test_blank_bash_file.sh"
        path_to_test_bashrc_altered = self.project_directory + "\\test\\test_files\\test_blank_bash_file_one_var.sh"
        self.assertFalse(self.two_text_files_equal(path_to_test_bashrc_original, path_to_test_bashrc_altered))
        args = self.parser.parse_args(["-k", "test_var", "-v", "test", "-p", path_to_test_bashrc_original])
        main(args)
        original_lines = open(path_to_test_bashrc_original, 'r').readlines()
        expected_line = "export TEST_VAR=test\n"
        actual_line = original_lines[2]
        self.assertEqual(expected_line, actual_line)

    def test_remove_var(self):
        path_to_test_bashrc_no_var = self.project_directory + "\\test\\test_files\\test_blank_bash_file.sh"
        path_to_test_bashrc_one_var = self.project_directory + "\\test\\test_files\\test_blank_bash_file_one_var.sh"
        self.assertFalse(self.two_text_files_equal(path_to_test_bashrc_no_var, path_to_test_bashrc_one_var))
        self.parser.parse_args(["-r", "TEST_VAR"])
        original_lines = open(path_to_test_bashrc_no_var).readlines()
        for line in original_lines:
            if "TEST_VAR" in line:
                raise AssertionError("TEST_VAR not removed")

if __name__ == '__main__':
    unittest.main()