# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the generate_test_project.py script.
"""

import unittest
from pathlib import Path
from unittest.mock import call, patch

from ts_backend_check.cli.generate_test_project import (
    INTERNAL_TEST_PROJECT_DIR_PATH,
    PATH_SEPARATOR,
    generate_test_project,
)


class TestGenerateTestProject(unittest.TestCase):
    """
    Test cases for the generate_test_project function.
    """

    @patch("pathlib.Path.is_dir", return_value=False)
    @patch("shutil.copytree")
    @patch("builtins.print")
    @patch("pathlib.Path.is_file", return_value=False)
    def test_generate_when_directory_does_not_exist(
        self, mock_is_file, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests that the test project are generated when the destination directory does not exist.
        """
        generate_test_project()

        mock_is_dir.assert_called_with()
        mock_copytree.assert_called_once_with(
            INTERNAL_TEST_PROJECT_DIR_PATH,
            Path("./ts_backend_check_test_project/"),
            dirs_exist_ok=True,
        )
        self.assertIn(
            call(
                f"Generating testing project for ts-backend-check in .{PATH_SEPARATOR}ts_backend_check_test_project{PATH_SEPARATOR} ..."
            ),
            mock_print.call_args_list,
        )
        self.assertIn(
            call("The test project has been successfully generated."),
            mock_print.call_args_list,
        )
        self.assertIn(
            call(
                "Please generate one with the 'ts-backend-check --generate-config-file' command."
            ),
            mock_print.call_args_list,
        )

    @patch("pathlib.Path.is_dir", return_value=True)
    @patch("shutil.copytree")
    @patch("builtins.print")
    def test_generate_when_directory_exists(
        self, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests that the test project are not generated when the destination directory already exists.
        """
        generate_test_project()

        mock_is_dir.assert_called_with()
        mock_copytree.assert_not_called()
        mock_print.assert_called_once_with(
            f"Test project for ts-backend-check already exist in .{PATH_SEPARATOR}ts_backend_check_test_project{PATH_SEPARATOR} and will not be regenerated."
        )

    @patch("pathlib.Path.is_dir", return_value=False)
    @patch("shutil.copytree")
    @patch("builtins.print")
    @patch("pathlib.Path.is_file", side_effect=[True, True])
    def test_prints_correct_message_when_yaml_exists(
        self, mock_is_file, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests the output message when a .ts-backend-check.yaml file exists.
        """
        generate_test_project()
        mock_print.assert_any_call(
            "You can set which one to test in the .ts-backend-check.yaml file."
        )

    @patch("pathlib.Path.is_dir", return_value=False)
    @patch("shutil.copytree")
    @patch("builtins.print")
    @patch("pathlib.Path.is_file", side_effect=[False, True, False, True])
    def test_prints_correct_message_when_yml_exists(
        self, mock_is_file, mock_print, mock_copytree, mock_is_dir
    ):
        """
        Tests the output message when a .ts-backend-check.yml file exists.
        """
        generate_test_project()
        mock_print.assert_any_call(
            "You can set which one to test in the .ts-backend-check.yml file."
        )


if __name__ == "__main__":
    unittest.main()
