# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI config file generation functionality.
"""

from unittest.mock import patch

from ts_backend_check.cli.config import (
    configure_paths,
    create_config,
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
    monkeypatch.setattr("ts_backend_check.cli.config.__file__", str(dummy_script))

    assert path_exists("nonexistent.py") is False


def test_write_config_creates_yaml(tmp_path, monkeypatch):
    config = {
        "auth": {
            "backend_model_path": "backend/models.py",
            "frontend_interface_path": "frontend/auth.ts",
        }
    }

    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", yaml_file)

    write_config(config)

    assert yaml_file.exists()
    content = yaml_file.read_text()
    assert "auth:" in content
    assert "backend_model_path" in content
    assert "frontend_interface_path" in content


@patch("ts_backend_check.cli.config.path_exists", return_value=True)
def test_configure_paths_auth_empty_first(mock_path, tmp_path, monkeypatch, capsys):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", yaml_file)
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    inputs = iter(
        [
            "",  # key
            "auth",
            "backend/models.py",  # backend path
            "frontend/auth.ts",  # frontend path
            "n",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_paths()
    captured = capsys.readouterr()
    assert "Key cannot be empty. Please try again." in captured.out


@patch("ts_backend_check.cli.config.path_exists", return_value=True)
def test_configure_paths_empty_backend_path(mock_path, tmp_path, monkeypatch, capsys):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", yaml_file)
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    inputs = iter(
        [
            "",  # key
            "auth",
            "",
            "backend/models.py",  # backend path
            "frontend/auth.ts",  # frontend path
            "n",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_paths()
    captured = capsys.readouterr()
    assert "Path cannot be empty." in captured.out


@patch("ts_backend_check.cli.config.path_exists", return_value=True)
def test_configure_paths_empty_frontend_path(mock_path, tmp_path, monkeypatch, capsys):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", yaml_file)
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    inputs = iter(
        [
            "",  # key
            "auth",
            "backend/models.py",  # backend path
            "",
            "frontend/auth.ts",  # frontend path
            "n",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_paths()
    captured = capsys.readouterr()
    assert "Path cannot be empty." in captured.out


@patch("ts_backend_check.cli.config.path_exists", return_value=True)
def test_configure_paths_valid_flow(mock_path, tmp_path, monkeypatch):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", yaml_file)
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    inputs = iter(
        [
            "auth",  # key
            "backend/models.py",  # backend path
            "frontend/auth.ts",  # frontend path
            "n",  # finish
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_paths()

    assert yaml_file.exists()
    content = yaml_file.read_text()
    assert "auth:" in content
    assert "backend/models.py" in content
    assert "frontend/auth.ts" in content


@patch(
    "ts_backend_check.cli.config.path_exists", side_effect=[False, True, False, True]
)
def test_configure_paths_invalid_then_valid(mock_path, tmp_path, monkeypatch):
    yaml_file = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", yaml_file)
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    inputs = iter(
        [
            "auth",  # key
            "invalid/backend.py",  # backend invalid
            "valid/backend.py",  # backend valid
            "invalid/frontend.ts",  # frontend invalid
            "valid/frontend.ts",  # frontend valid
            "n",  # done
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    configure_paths()

    assert yaml_file.exists()
    content = yaml_file.read_text()
    assert "valid/backend.py" in content
    assert "valid/frontend.ts" in content


@patch("ts_backend_check.cli.config.configure_paths")
def test_create_config_creates_new(mock_configure, tmp_path, monkeypatch):
    config_path = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr(
        "ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", config_path
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    if config_path.exists():
        config_path.unlink()

    create_config()

    mock_configure.assert_called_once()


@patch("ts_backend_check.cli.config.configure_paths")
def test_create_config_existing_user_skips(mock_configure, tmp_path, monkeypatch):
    config_path = tmp_path / ".ts-backend-check.yaml"
    config_path.write_text("existing content")

    monkeypatch.setattr(
        "ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", config_path
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    monkeypatch.setattr("builtins.input", lambda _: "n")

    create_config()

    mock_configure.assert_not_called()


# @patch("builtins.input", side_effect=KeyboardInterrupt)
# def test_create_config_simulate_keyboard_interrupt(mock_input, capsys):
#     result = create_config()
#     assert result is None
#
#     captured_err = capsys.readouterr()
#     assert "\n\nConfiguration cancelled by user." in captured_err.out
