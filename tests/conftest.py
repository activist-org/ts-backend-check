# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
import yaml

from ts_backend_check.utils import get_config_file_path

YAML_CONFIG_FILE_PATH = get_config_file_path()
with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# MARK: Valid

valid_django_models = config["valid_model"]["backend_model_path"]
valid_ts_interfaces = [Path(p) for p in config["valid_model"]["ts_interface_paths"]]
valid_check_blank_models = config["valid_model"]["check_blank_model_fields"]
valid_backend_to_ts_conversions = config["valid_model"][
    "backend_to_ts_model_name_conversions"
]


@pytest.fixture
def return_valid_django_models():
    return str(valid_django_models)


@pytest.fixture
def return_valid_concatenated_types_file():
    concatenated_types_file = ""
    for p in valid_ts_interfaces:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    return concatenated_types_file


@pytest.fixture
def return_valid_check_blank_models():
    return valid_check_blank_models


@pytest.fixture
def return_valid_backend_to_ts_conversions():
    return valid_backend_to_ts_conversions


# MARK: Invalid

invalid_django_models = config["invalid_model"]["backend_model_path"]
invalid_ts_interfaces = [Path(p) for p in config["invalid_model"]["ts_interface_paths"]]
invalid_check_blank_models = config["invalid_model"]["check_blank_model_fields"]
invalid_backend_to_ts_conversions = config["invalid_model"][
    "backend_to_ts_model_name_conversions"
]


@pytest.fixture
def return_invalid_django_models():
    return str(invalid_django_models)


@pytest.fixture
def return_invalid_concatenated_types_file():
    concatenated_types_file = ""
    for p in invalid_ts_interfaces:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    return concatenated_types_file


@pytest.fixture
def return_invalid_check_blank_models():
    return invalid_check_blank_models


@pytest.fixture
def return_invalid_backend_to_ts_conversions():
    return invalid_backend_to_ts_conversions
