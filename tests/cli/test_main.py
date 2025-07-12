# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
import sys


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
    assert (
        result.stdout.strip()
        == "All models are synced with their corresponding TypeScript interfaces."
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
        result.stdout
        == "nonexistent.py that should contain the backend models does not exist. Please check and try again.\n"
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
        result.stdout
        == "nonexistent.ts file that should contain the TypeScript types does not exist. Please check and try again.\n"
    )
