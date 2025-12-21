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
        # Create temporary backend model and TypeScript files that match.
        model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
"""
        type_content = """export interface TestModel {
    name: string;
}
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            model_file = Path(tmpdir) / "test_model.py"
            model_file.write_text(model_content)

            ts_file = Path(tmpdir) / "test_type.ts"
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
        self.assertEqual(
            result.stdout.strip().replace("\n", ""),
            "✅ Success: All models are synced with their corresponding TypeScript interfaces.",
        )

    def test_cli_check_command_with_missing_fields(self):
        # Create a model with fields and a TS file missing a field.
        model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
"""
        type_content = """export interface TestModel {
    name: string;
}
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            model_file = Path(tmpdir) / "test_model.py"
            model_file.write_text(model_content)

            ts_file = Path(tmpdir) / "test_type.ts"
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

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().replace("\n", ""),
            "nonexistent.py that should contain the backend models does not exist. Please check and try again.",
        )

    def test_cli_check_command_with_nonexistent_ts_files(self):
        # Create a valid backend model file but point TS file to a nonexistent path.
        model_content = """from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            model_file = Path(tmpdir) / "test_model.py"
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

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().replace("\n", ""),
            "nonexistent.ts file that should contain the TypeScript types does not exist. Please check and try again.",
        )


if __name__ == "__main__":
    unittest.main()
