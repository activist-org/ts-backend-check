# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for the CLI config file generation functionality.
"""

import builtins
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from ts_backend_check.cli.config import (
    YAML_CONFIG_FILE_PATH,
    create_config,
    path_exits,
    write_config,
)


def test_path_exits_false(tmp_path):
    with patch("ts_backend_check.cli.config.__file__", str(tmp_path / "dummy.py")):
        assert path_exits("missing.py") is False


def test_write_config_writes_yaml(tmp_path, monkeypatch):
    config = {
        "auth": {
            "backend_model_path": "backend/auth/models.py",
            "frontend_interface_path": "frontend/interfaces/auth.d.ts",
        }
    }

    fake_path = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", fake_path)

    write_config(config)

    content = fake_path.read_text()
    assert "auth:" in content
    assert "backend_model_path: backend/auth/models.py" in content
    assert "frontend_interface_path: frontend/interfaces/auth.d.ts" in content


def test_create_config_creates_file_if_not_exists(tmp_path, monkeypatch):
    fake_path = tmp_path / ".ts-backend-check.yaml"
    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", fake_path)

    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "dummy.py")
    )

    monkeypatch.setattr("builtins.input", lambda _: "n")

    create_config()
    assert fake_path.exists()
    assert fake_path.read_text() == ""


def test_create_config_skips_reconfig_if_user_says_no(tmp_path, monkeypatch):
    fake_yaml_path = tmp_path / ".ts-backend-check.yaml"
    fake_yaml_path.write_text("# existing config")

    monkeypatch.setattr(
        "ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", fake_yaml_path
    )
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/script.py")
    )

    with patch("builtins.input", return_value="n"):
        create_config()

    assert fake_yaml_path.read_text() == "# existing config"


@patch("ts_backend_check.cli.config.path_exits", return_value=True)
def test_create_config_reconfigures_correctly(mock_path_exits, tmp_path, monkeypatch):
    yaml_path = tmp_path / ".ts-backend-check.yaml"
    yaml_path.write_text("# old content")

    monkeypatch.setattr("ts_backend_check.cli.config.YAML_CONFIG_FILE_PATH", yaml_path)
    monkeypatch.setattr(
        "ts_backend_check.cli.config.__file__", str(tmp_path / "a/b/c/d/fake.py")
    )

    # Simulate input sequence:
    # - reconfigure = 'y'
    # - key = 'auth'
    # - backend path
    # - frontend path
    # - continue? 'n'
    input_sequence = iter(
        [
            "y",  # Reconfigure?
            "auth",  # Key
            "backend/models.py",  # Backend path
            "frontend/auth.ts",  # Frontend path
            "n",  # Continue? no
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    create_config()

    content = yaml_path.read_text()
    assert "auth:" in content
    assert "backend_model_path: backend/models.py" in content
    assert "frontend_interface_path: frontend/auth.ts" in content
