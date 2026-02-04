# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI main functionality rewritten in unittest style.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ts_backend_check.cli.main import config, get_config_file_path, main


class TestCliMain(unittest.TestCase):
    """
    Test suite for the main CLI entry point of ts-backend-check.
    """

    def setUp(self) -> None:
        """
        Create a temporary directory for each test to mimic pytest's tmp_path.
        """
        # Create a temporary directory object
        self._temp_dir_obj = tempfile.TemporaryDirectory()
        # Convert it to a pathlib.Path object for ease of use
        self.tmp_path = Path(self._temp_dir_obj.name)
        # Ensure it gets cleaned up after the test runs
        self.addCleanup(self._temp_dir_obj.cleanup)

    def test_get_config_file_path_yaml_exists(self) -> None:
        """
        Test that .yaml file is preferred when both .yaml and .yml exist.
        """
        yaml_file = self.tmp_path / ".ts-backend-check.yaml"
        yml_file = self.tmp_path / ".ts-backend-check.yml"

        yaml_file.write_text("yaml: true", encoding="utf-8")
        yml_file.write_text("yml: true", encoding="utf-8")

        # Mock CWD_PATH to use self.tmp_path.
        with patch("ts_backend_check.cli.main.CWD_PATH", self.tmp_path):
            result = get_config_file_path()
            self.assertEqual(result.name, ".ts-backend-check.yaml")
            self.assertTrue(result.is_file())

    def test_get_config_file_path_only_yml_exists(self) -> None:
        """
        Test that .yml file is found when only .yml exists.
        """
        yml_file = self.tmp_path / ".ts-backend-check.yml"
        yml_file.write_text("yml: true", encoding="utf-8")

        # Mock CWD_PATH to use self.tmp_path.
        with patch("ts_backend_check.cli.main.CWD_PATH", self.tmp_path):
            result = get_config_file_path()
            self.assertEqual(result.name, ".ts-backend-check.yml")
            self.assertTrue(result.is_file())

    def test_get_config_file_path_neither_exists(self) -> None:
        """
        Test that .yaml is returned as default when neither file exists.
        """
        # Mock CWD_PATH to use self.tmp_path.
        with patch("ts_backend_check.cli.main.CWD_PATH", self.tmp_path):
            result = get_config_file_path()
            self.assertEqual(result.name, ".ts-backend-check.yaml")
            self.assertFalse(result.is_file())

    @patch("ts_backend_check.cli.main.argparse.ArgumentParser.print_help")
    def test_main_no_args(self, mock_print_help):
        """
        Test that `print_help` is called when no arguments are provided.
        """
        with patch("sys.argv", ["ts-backend-check"]):
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 0)
        mock_print_help.assert_called_once()

    @patch("ts_backend_check.cli.main.upgrade_cli")
    def test_main_upgrade(self, mock_upgrade_cli):
        """
        Test that `upgrade_cli` is called with the --upgrade flag.
        """
        with patch("sys.argv", ["ts-backend-check", "--upgrade"]):
            main()

        mock_upgrade_cli.assert_called_once()

    @patch("ts_backend_check.cli.main.generate_config_file")
    def test_main_generate_config_file(self, mock_generate_config_file):
        """
        Test that `generate_config_file` is called with the --generate-config-file flag.
        """
        with patch("sys.argv", ["ts-backend-check", "--generate-config-file"]):
            main()

        mock_generate_config_file.assert_called_once()

    def test_cli_check_command_success(self):
        """
        Successful run when backend models and TypeScript types are in sync.
        """
        model_name = "valid_model"
        result = subprocess.run(
            [
                sys.executable,
                "src/ts_backend_check/cli/main.py",
                "-m",
                model_name,
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        stdout_flat = result.stdout.strip().replace("\n", "")
        self.assertIn(
            "✅ Success: All backend models are synced with their corresponding TypeScript",
            stdout_flat,
        )
        self.assertIn(f"interfaces for the provided '{model_name}' files.", stdout_flat)

    def test_cli_check_command_with_missing_fields(self):
        """
        CLI should return non-zero exit code when TypeScript types are missing fields present
        in the Django model.
        """
        result = subprocess.run(
            [
                sys.executable,
                "src/ts_backend_check/cli/main.py",
                "-m",
                "invalid_model",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)

    def test_cli_check_command_with_invalid_identifier(self):
        """
        When the model does not exist, CLI should print an informative message
        and exit with code 1.
        """
        result = subprocess.run(
            [
                sys.executable,
                "src/ts_backend_check/cli/main.py",
                "-m",
                "invalid_identifier",
            ],
            capture_output=True,
            text=True,
        )

        stdout_flat = result.stdout.strip().replace("\n", "")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            stdout_flat,
            "invalid_identifier is not an index within the .ts-backend-check.yaml configuration file. Please check the defined models and try again.",
        )

    def test_cli_check_command_with_nonexistent_backend_model_files(self):
        """
        When the model does not exist, CLI should print an informative message
        and exit with code 1.
        """
        result = subprocess.run(
            [
                sys.executable,
                "src/ts_backend_check/cli/main.py",
                "-m",
                "invalid_backend_model_path",
            ],
            capture_output=True,
            text=True,
        )

        stdout_flat = result.stdout.strip().replace("\n", "")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            stdout_flat,
            "❌ invalid_path_to_models.py that should contain the 'invalid_backend_model_path' backend models does not exist. Please check the ts-backend-check configuration file and try again.",
        )

    def test_cli_check_command_with_nonexistent_ts_files(self):
        """
        When TypeScript file does not exist, CLI should print an informative message
        and exit with code 1.
        """
        result = subprocess.run(
            [
                sys.executable,
                "src/ts_backend_check/cli/main.py",
                "-m",
                "invalid_typescript_interface_path",
            ],
            capture_output=True,
            text=True,
        )

        stdout_flat = result.stdout.strip().replace("\n", "")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(
            stdout_flat,
            "❌ invalid_path_to_interfaces.ts that should contain the 'invalid_typescript_interface_path' TypeScript types does not exist. Please check the ts-backend-check configuration file and try again.",
        )

    def test_version_flag_exits_with_zero(self):
        """
        --version should trigger argparse's version action and exit with code 0.
        """
        with patch(
            "ts_backend_check.cli.main.get_version_message", return_value="vX.Y.Z"
        ):
            with patch("sys.argv", ["ts-backend-check", "--version"]):
                with self.assertRaises(SystemExit) as cm:
                    main()
        self.assertEqual(cm.exception.code, 0)

    def test_model_invokes_check_files_and_print_results(self):
        """
        Providing --model should call the check_files_and_print_results function with the provided arg.
        """
        with patch(
            "ts_backend_check.cli.main.check_files_and_print_results"
        ) as check_files_and_print_results_model:
            with patch("sys.argv", ["ts-backend-check", "--model", "valid_model"]):
                main()

        check_files_and_print_results_model.assert_called_once_with(
            identifier="valid_model",
            backend_model_file_path=Path(config["valid_model"]["backend_model_path"]),
            ts_interface_file_path=Path(config["valid_model"]["ts_interface_path"]),
            check_blank=True,
            model_name_conversions={"EventModel": ["Event"]},
        )

    def test_typechecker_no_missing_fields_prints_success(self):
        """
        When TypeChecker.check() returns an empty list, the CLI should print the success message.
        """
        with patch("ts_backend_check.cli.main.TypeChecker") as MockTypeChecker:
            MockTypeChecker.return_value.check.return_value = []

            with patch("ts_backend_check.cli.main.rprint") as mock_rprint:
                with patch(
                    "sys.argv",
                    [
                        "ts-backend-check",
                        "-m",
                        "valid_model",
                    ],
                ):
                    main()

            # The success message is printed once with the exact green-markup string.
            expected = (
                "[green]✅ Success: All backend models are synced with their corresponding "
                "TypeScript interfaces for the provided 'valid_model' files.[/green]"
            )
            # Ensure rprint was called and the final call contains the expected message.
            self.assertTrue(mock_rprint.called)
            self.assertEqual(mock_rprint.call_args_list[-1][0][0], expected)

    def test_typechecker_missing_fields_exits_with_one_and_prints_errors(self):
        """
        When TypeChecker.check() returns missing fields, the CLI should print errors
        and exit with status code 1.
        """
        # Patch TypeChecker so its .check() returns a list of missing-field messages.
        with patch("ts_backend_check.cli.main.TypeChecker") as MockTypeChecker:
            MockTypeChecker.return_value.check.return_value = [
                "TestModel.age is missing in TypeScript type"
            ]

            # Make Text.from_markup return the raw string to simplify assertions.
            with patch(
                "ts_backend_check.cli.main.Text.from_markup",
                side_effect=lambda s: s,
            ):
                with patch("ts_backend_check.cli.main.rprint") as mock_rprint:
                    with patch(
                        "sys.argv",
                        [
                            "ts-backend-check",
                            "-m",
                            "invalid_model",
                        ],
                    ):
                        with self.assertRaises(SystemExit) as cm:
                            main()

        # Check that the exit code is 1.
        self.assertEqual(cm.exception.code, 1)

        # Ensure rprint was called and that at least one call contains the error header text.
        self.assertTrue(mock_rprint.called)
        calls = [call_args[0][0] for call_args in mock_rprint.call_args_list]

        # Convert all call args to strings for easier substring checks.
        calls_str = [str(c) for c in calls]
        self.assertTrue(
            any(
                "There are inconsistencies between the provided backend models and TypeScript interfaces"
                in s
                or "ts-backend-check error" in s
                for s in calls_str
            ),
            msg=f"Expected error header in rprint calls, got: {calls_str}",
        )


if __name__ == "__main__":
    unittest.main()
