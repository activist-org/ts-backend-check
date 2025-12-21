# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI main functionality rewritten in unittest style.
"""

import subprocess
import sys
import unittest
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


def test_cli_check_command_success(temp_django_model, temp_typescript_file):
    result = subprocess.run(
        [
            sys.executable,
            "src/ts_backend_check/cli/main.py",
            "-bmf",
            temp_django_model,
            "-tsf",
            temp_typescript_file,
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    # Note: Don't include check mark as Windows isn't rendering it.
    assert (
        "Success: All models are synced with their corresponding TypeScript interfaces."
        in result.stdout.strip().replace("\n", "")
    )


def test_cli_check_command_with_missing_fields(tmp_path):
    # Create a model with fields.
    model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()"""

    model_file = tmp_path / "test_model.py"
    model_file.write_text(model_content)

    # Create a type with missing field.
    type_content = """export interface Test {
    name: string;
}"""

    type_file = tmp_path / "test_type.ts"
    type_file.write_text(type_content)

    result = subprocess.run(
        [
            sys.executable,
            "src/ts_backend_check/cli/main.py",
            "-bmf",
            model_file,
            "-tsf",
            type_file,
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1


def test_cli_check_command_with_nonexistent_backend_model_files():
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

    print("stdout: ", result.stdout.strip())
    print("Stderr: ", result.stderr)

    assert result.returncode == 0
    assert (
        result.stdout.strip().replace("\n", "")
        == "nonexistent.py that should contain the backend models does not exist. Please check and try again."
    )


def test_cli_check_command_with_nonexistent_ts_files(temp_django_model):
    result = subprocess.run(
        [
            sys.executable,
            "src/ts_backend_check/cli/main.py",
            "-bmf",
            temp_django_model,
            "-tsf",
            "nonexistent.ts",
        ],
        capture_output=True,
        text=True,
    )

    print("stdout: ", result.stdout.strip())
    print("Stderr: ", result.stderr)

    assert result.returncode == 0
    assert (
        result.stdout.strip().replace("\n", "")
        == "nonexistent.ts file that should contain the TypeScript types does not exist. Please check and try again."
    )
