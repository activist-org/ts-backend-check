# SPDX-License-Identifier: GPL-3.0-or-later

from click.testing import CliRunner

from ts_backend_check.cli.main import check


def test_cli_check_command_success(temp_django_model, temp_typescript_file):
    runner = CliRunner()
    result = runner.invoke(check, ["check", temp_django_model, temp_typescript_file])

    assert result.exit_code == 0
    assert "All model fields are properly typed in TypeScript!" in result.output


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

    runner = CliRunner()
    result = runner.invoke(check, ["check", str(model_file), str(type_file)])

    assert result.exit_code == 1
    assert "Missing TypeScript fields found:" in result.output
    assert "age" in result.output


def test_cli_check_command_with_nonexistent_files():
    runner = CliRunner()
    result = runner.invoke(check, ["check", "nonexistent.py", "nonexistent.ts"])

    assert result.exit_code == 2
    assert "does not exist" in result.output


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(check, ["--version"])

    assert result.exit_code == 0
    assert result.output.strip().startswith("cli, version")
