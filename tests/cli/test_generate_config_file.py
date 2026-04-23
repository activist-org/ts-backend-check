# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI configuration file generation functionality.
"""

from unittest.mock import patch

from ts_backend_check.cli.generate_config_file import (
    configure_model_interface_arguments,
    generate_config_file,
    path_exists,
    write_config,
)


def test_path_exists_true(tmp_path, monkeypatch):
    dummy_script = tmp_path / "a/b/c/d/script.py"
    dummy_script.parent.mkdir(parents=True, exist_ok=True)
    dummy_script.touch()

    result = path_exists(dummy_script)
    assert result is True


def test_path_exists_false(tmp_path, monkeypatch):
    dummy_script = tmp_path / "a/b/c/d/script.py"
    dummy_script.parent.mkdir(parents=True)
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__", str(dummy_script)
    )

    assert path_exists("nonexistent.py") is False


def test_write_config_creates_yaml(tmp_path, monkeypatch):
    config = {
        "auth": {
            "backend_model_path": "backend/models.py",
            "frontend_interface_path": "frontend/auth.ts",
        }
    }

    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", yaml_file
    )

    write_config(config)

    assert yaml_file.exists()

    content = yaml_file.read_text()
    assert "auth:" in content
    assert "backend_model_path" in content
    assert "frontend_interface_path" in content


@patch("ts_backend_check.cli.generate_config_file.path_exists", return_value=True)
def test_configure_model_interface_arguments_identifier_empty_first(
    mock_path, tmp_path, monkeypatch, capsys
):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", yaml_file
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__",
        str(tmp_path / "a/b/c/d/script.py"),
    )

    inputs = iter(
        [
            "",  # empty identifier
            "valid_model",  # identifier
            "src/ts_backend_check/test_project/backend/models.py",  # backend path
            "src/ts_backend_check/test_project/frontend/valid_interfaces.ts",  # frontend path
            "",  # check blank
            "",  # ignore models
            "",  # no conversions
            "",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_model_interface_arguments()
    captured = capsys.readouterr()
    assert (
        "The model-interface identifier cannot be empty. Please try again."
        in captured.out
    )


@patch("ts_backend_check.cli.generate_config_file.path_exists", return_value=True)
def test_configure_model_interface_arguments_empty_backend_path(
    mock_path, tmp_path, monkeypatch, capsys
):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", yaml_file
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__",
        str(tmp_path / "a/b/c/d/script.py"),
    )

    inputs = iter(
        [
            "valid_model",  # identifier
            "",  # empty backend path
            "src/ts_backend_check/test_project/backend/models.py",  # backend path
            "src/ts_backend_check/test_project/frontend/valid_interfaces.ts",  # frontend path
            "",  # check blank
            "",  # ignore models
            "",  # no conversions
            "",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_model_interface_arguments()
    captured = capsys.readouterr()
    assert (
        "The path for the Django models.py file cannot be empty. Please try again."
        in captured.out
    )


@patch("ts_backend_check.cli.generate_config_file.path_exists", return_value=True)
def test_configure_model_interface_arguments_empty_typescript_path(
    mock_path, tmp_path, monkeypatch, capsys
):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", yaml_file
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__",
        str(tmp_path / "a/b/c/d/script.py"),
    )

    inputs = iter(
        [
            "valid_model",  # identifier
            "src/ts_backend_check/test_project/backend/models.py",  # backend path
            "",  # empty ts path
            "src/ts_backend_check/test_project/frontend/valid_interfaces.ts",  # frontend path
            "",  # check blank
            "",  # ignore models
            "",  # no conversions
            "",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_model_interface_arguments()
    captured = capsys.readouterr()
    assert (
        "The path for the TypeScript interface file cannot be empty. Please try again."
        in captured.out
    )


@patch("ts_backend_check.cli.generate_config_file.path_exists", return_value=True)
def test_configure_model_interface_arguments_valid_flow(
    mock_path, tmp_path, monkeypatch
):
    """
    Test a valid generation of a configuration file including model-interface name conversions.
    """
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", yaml_file
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__",
        str(tmp_path / "a/b/c/d/script.py"),
    )

    inputs = iter(
        [
            "valid_model",  # identifier
            "src/ts_backend_check/test_project/backend/models.py",  # backend path
            "src/ts_backend_check/test_project/frontend/valid_interfaces.ts",  # frontend path
            "y",  # check blank
            "n",  # ignore models
            "y",  # include conversions
            "UserModel",
            "User",
            "n",  # only one conversion
            "n",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_model_interface_arguments()

    assert yaml_file.exists()

    content = yaml_file.read_text()
    assert "valid_model:" in content
    assert "src/ts_backend_check/test_project/backend/models.py" in content
    assert "src/ts_backend_check/test_project/frontend/valid_interfaces.ts" in content
    assert "check_blank_model_fields: true" in content
    assert "UserModel:" and "- User" in content


@patch(
    "ts_backend_check.cli.generate_config_file.path_exists",
    side_effect=[
        False,
        True,
        False,
        True,
    ],  # 1st fail, 2nd pass, 3rd fail, 4th pass
)
def test_configure_model_interface_arguments_invalid_then_valid(
    mock_path, tmp_path, monkeypatch
):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", yaml_file
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__",
        str(tmp_path / "a/b/c/d/script.py"),
    )

    inputs = iter(
        [
            "valid_model",  # identifier
            "invalid_path_to_models_path.py",
            "src/ts_backend_check/test_project/backend/models.py",  # backend path
            "invalid_path_to_interfaces_path.ts",
            "src/ts_backend_check/test_project/frontend/valid_interfaces.ts",  # frontend path
            "not_y_or_n_or_blank",  # check blank
            "n",  # check blank
            "n",  # ignore models
            "",  # no conversions
            "",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_model_interface_arguments()

    assert yaml_file.exists()

    content = yaml_file.read_text()
    assert "valid_model:" in content
    assert "src/ts_backend_check/test_project/backend/models.py" in content
    assert "src/ts_backend_check/test_project/frontend/valid_interfaces.ts" in content


@patch("ts_backend_check.cli.generate_config_file.configure_model_interface_arguments")
def test_generate_config_file_creates_new(mock_configure, tmp_path, monkeypatch):
    config_path = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__",
        str(tmp_path / "a/b/c/d/script.py"),
    )

    if config_path.exists():
        config_path.unlink()

    generate_config_file()

    mock_configure.assert_called_once()


@patch("ts_backend_check.cli.generate_config_file.configure_model_interface_arguments")
def test_generate_config_file_existing_user_skips(
    mock_configure, tmp_path, monkeypatch
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text("existing content")

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.__file__",
        str(tmp_path / "a/b/c/d/script.py"),
    )

    monkeypatch.setattr("builtins.input", lambda _: "n")

    generate_config_file()

    mock_configure.assert_not_called()


def test_config_file_is_valid_empty_file_returns_false(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text("")

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    result = config_file_is_valid()
    assert result is False

    out = capsys.readouterr().out.replace("\n", " ")
    assert "empty" in out


def test_config_file_is_valid_value_not_dict_returns_false(
    tmp_path, monkeypatch, capsys
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text("my_identifier: just_a_string\n")

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    result = config_file_is_valid()
    assert result is False

    out = capsys.readouterr().out.replace("\n", " ")
    assert "not" in out and "dictionary" in out
    assert "my_identifier" in out


def test_config_file_is_valid_backend_model_path_none_returns_false(
    tmp_path, monkeypatch, capsys
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text(
        "my_identifier:\n"
        "  backend_model_path: null\n"
        "  ts_interface_paths: some/path.ts\n"
    )

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    result = config_file_is_valid()
    assert result is False

    out = capsys.readouterr().out.replace("\n", " ")
    assert "backend_model_path" in out
    assert "my_identifier" in out


def test_config_file_is_valid_ts_interface_paths_none_returns_false(
    tmp_path, monkeypatch, capsys
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text(
        "my_identifier:\n"
        "  backend_model_path: some/models.py\n"
        "  ts_interface_paths: null\n"
    )

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    result = config_file_is_valid()
    assert result is False

    out = capsys.readouterr().out.replace("\n", " ")
    assert "ts_interface_paths" in out
    assert "my_identifier" in out


def test_config_file_is_valid_single_valid_identifier_returns_true(
    tmp_path, monkeypatch
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text(
        "my_identifier:\n"
        "  backend_model_path: some/models.py\n"
        "  ts_interface_paths: some/interfaces.ts\n"
    )

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    assert config_file_is_valid() is True


def test_config_file_is_valid_multiple_valid_identifiers_returns_true(
    tmp_path, monkeypatch
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text(
        "identifier_one:\n"
        "  backend_model_path: app/models.py\n"
        "  ts_interface_paths: app/types.ts\n"
        "identifier_two:\n"
        "  backend_model_path: other/models.py\n"
        "  ts_interface_paths: other/types.ts\n"
    )

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    assert config_file_is_valid() is True


def test_config_file_is_valid_second_identifier_not_dict_returns_false(
    tmp_path, monkeypatch, capsys
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text(
        "good_identifier:\n"
        "  backend_model_path: app/models.py\n"
        "  ts_interface_paths: app/types.ts\n"
        "bad_identifier: not_a_dict\n"
    )

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    result = config_file_is_valid()
    assert result is False

    out = capsys.readouterr().out.replace("\n", " ")
    assert "bad_identifier" in out
    assert "not" in out and "dictionary" in out


def test_config_file_is_valid_second_identifier_missing_backend_path_returns_false(
    tmp_path, monkeypatch, capsys
):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text(
        "good_identifier:\n"
        "  backend_model_path: app/models.py\n"
        "  ts_interface_paths: app/types.ts\n"
        "bad_identifier:\n"
        "  backend_model_path: null\n"
        "  ts_interface_paths: other/types.ts\n"
    )

    monkeypatch.setattr(
        "ts_backend_check.cli.generate_config_file.YAML_CONFIG_FILE_PATH", config_path
    )

    from ts_backend_check.cli.generate_config_file import config_file_is_valid

    result = config_file_is_valid()
    assert result is False

    out = capsys.readouterr().out.replace("\n", " ")
    assert "bad_identifier" in out
    assert "backend_model_path" in out
