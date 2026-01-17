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

from ts_backend_check.cli.main import main


class TestCliMain(unittest.TestCase):
    """
    Test suite for the main CLI entry point of ts-backend-check.
    """

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

    @patch("ts_backend_check.cli.main.create_config")
    def test_main_generate_config_file(self, mock_generate_config_file):
        """
        Test that `create_config` is called with the --configure flag.
        """
        with patch("sys.argv", ["ts-backend-check", "--configure"]):
            main()

        mock_generate_config_file.assert_called_once()

    def test_cli_check_command_success(self):
        """
        Successful run when backend models and TypeScript types are in sync.
        """
        model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
"""
        type_content = """export interface TestModel {
    name: string;
    age: number;
}
"""

        with tempfile.TemporaryDirectory() as td:
            model_file = Path(td) / "test_model.py"
            ts_file = Path(td) / "test_model.ts"
            model_file.write_text(model_content)
            ts_file.write_text(type_content)

            result = subprocess.run(
                [
                    sys.executable,
                    "src/ts_backend_check/cli/main.py",
                    "-bmf",
                    str(model_file),
                    "-tsf",
                    str(ts_file),
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
        self.assertIn("interfaces for the provided files.", stdout_flat)

    def test_cli_check_command_with_missing_fields(self):
        """
        CLI should return non-zero when TypeScript types are missing fields present
        in the Django model.
        """
        model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
"""
        type_content = """export interface TestModel {
    name: string;
}
"""

        with tempfile.TemporaryDirectory() as td:
            model_file = Path(td) / "test_model.py"
            ts_file = Path(td) / "test_type.ts"
            model_file.write_text(model_content)
            ts_file.write_text(type_content)

            result = subprocess.run(
                [
                    sys.executable,
                    "src/ts_backend_check/cli/main.py",
                    "-bmf",
                    str(model_file),
                    "-tsf",
                    str(ts_file),
                ],
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 1)

    def test_cli_check_command_with_nonexistent_backend_model_files(self):
        """
        When backend model file does not exist, CLI should print an informative message
        and exit with code 0 per original behavior.
        """
        result = subprocess.run(
            [
                sys.executable,
                "src/ts_backend_check/cli/main.py",
                "-bmf",
                "nonexistent.py",
                "-tsf",
                "nonexistent.ts",
            ],
            capture_output=True,
            text=True,
        )

        stdout_flat = result.stdout.strip().replace("\n", "")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            stdout_flat,
            "nonexistent.py that should contain the backend models does not exist. Please check and try again.",
        )

    def test_cli_check_command_with_nonexistent_ts_files(self):
        """
        When TypeScript file does not exist, CLI should print an informative message
        and exit with code 0 per original behavior.
        """
        model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
"""
        with tempfile.TemporaryDirectory() as td:
            model_file = Path(td) / "test_model.py"
            model_file.write_text(model_content)

            result = subprocess.run(
                [
                    sys.executable,
                    "src/ts_backend_check/cli/main.py",
                    "-bmf",
                    str(model_file),
                    "-tsf",
                    "nonexistent.ts",
                ],
                capture_output=True,
                text=True,
            )

        stdout_flat = result.stdout.strip().replace("\n", "")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            stdout_flat,
            "nonexistent.ts file that should contain the TypeScript types does not exist. Please check and try again.",
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

    def test_check_blank_invokes_check_blank(self):
        """
        Providing --check-blank should call the check_blank helper with the provided arg.
        """
        with patch("ts_backend_check.cli.main.check_blank") as mock_check_blank:
            with patch("sys.argv", ["ts-backend-check", "--check-blank", "models.py"]):
                main()
        mock_check_blank.assert_called_once_with("models.py")

    def test_typechecker_no_missing_fields_prints_success(self):
        """
        When TypeChecker.check() returns an empty list, the CLI should print the success message.
        """
        model_content = """from django.db import models
class TestModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
"""
        ts_content = """export interface TestModel {
    name: string;
    age: number;
}
"""

        with tempfile.TemporaryDirectory() as td:
            model_file = Path(td) / "test_model.py"
            ts_file = Path(td) / "test_model.ts"
            model_file.write_text(model_content)
            ts_file.write_text(ts_content)

            # Patch TypeChecker so its .check() returns an empty list (no missing fields).
            with patch("ts_backend_check.cli.main.TypeChecker") as MockTypeChecker:
                MockTypeChecker.return_value.check.return_value = []

                with patch("ts_backend_check.cli.main.rprint") as mock_rprint:
                    with patch(
                        "sys.argv",
                        [
                            "ts-backend-check",
                            "-bmf",
                            str(model_file),
                            "-tsf",
                            str(ts_file),
                        ],
                    ):
                        main()

            # The success message is printed once with the exact green-markup string.
            expected = (
                "[green]✅ Success: All backend models are synced with their corresponding "
                "TypeScript interfaces for the provided files.[/green]"
            )
            # Ensure rprint was called and the final call contains the expected message.
            self.assertTrue(mock_rprint.called)
            self.assertEqual(mock_rprint.call_args_list[-1][0][0], expected)

    def test_typechecker_missing_fields_exits_with_one_and_prints_errors(self):
        """
        When TypeChecker.check() returns missing fields, the CLI should print errors
        and exit with status code 1.
        """
        model_content = """from django.db import models
class TestModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
"""
        ts_content = """export interface TestModel {
    name: string;
}
"""

        with tempfile.TemporaryDirectory() as td:
            model_file = Path(td) / "test_model.py"
            ts_file = Path(td) / "test_type.ts"
            model_file.write_text(model_content)
            ts_file.write_text(ts_content)

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
                                "-bmf",
                                str(model_file),
                                "-tsf",
                                str(ts_file),
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
