# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest
import yaml

from tests.parsers.helpers import MinimalParser
from ts_backend_check.parsers.backend_parser import BackendModelParser, ModelData
from ts_backend_check.utils import get_config_file_path

YAML_CONFIG_FILE_PATH = get_config_file_path()
with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# MARK: Valid Models

# valid fastapi models
valid_fastapi_models = config["fastapi_model"]["backend_model_path"]
valid_fastapi_ts_interfaces = [
    Path(p) for p in config["fastapi_model"]["ts_interface_paths"]
]
valid_fastapi_check_blank_models = config["fastapi_model"]["check_blank_model_fields"]
valid_fastapi_backend_models_to_ignore = config["fastapi_model"][
    "backend_models_to_ignore"
]
valid_fastapi_backend_to_ts_conversions = config["fastapi_model"][
    "backend_to_ts_model_name_conversions"
]

# valid Django models
valid_django_models = config["django_model"]["backend_model_path"]
valid_django_ts_interfaces = [
    Path(p) for p in config["django_model"]["ts_interface_paths"]
]
valid_django_check_blank_models = config["django_model"]["check_blank_model_fields"]
valid_django_backend_models_to_ignore = config["django_model"][
    "backend_models_to_ignore"
]
valid_django_backend_to_ts_conversions = config["django_model"][
    "backend_to_ts_model_name_conversions"
]


# Fastapi Fixtures
@pytest.fixture
def return_valid_fastapi_models():
    return str(valid_fastapi_models)


@pytest.fixture
def return_valid_fastapi_concatenated_types_file():
    concatenated_types_file = ""
    for p in valid_fastapi_ts_interfaces:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    return concatenated_types_file


@pytest.fixture
def return_valid_fastapi_check_blank_models():
    return valid_fastapi_check_blank_models


@pytest.fixture
def return_valid_fastapi_backend_models_to_ignore():
    return valid_fastapi_backend_models_to_ignore


@pytest.fixture
def return_valid_fastapi_backend_to_ts_conversions():
    return valid_fastapi_backend_to_ts_conversions


# django fixtures
@pytest.fixture
def return_valid_django_models():
    return str(valid_django_models)


@pytest.fixture
def return_valid_django_concatenated_types_file():
    concatenated_types_file = ""
    for p in valid_django_ts_interfaces:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    return concatenated_types_file


@pytest.fixture
def return_valid_django_check_blank_models():
    return valid_django_check_blank_models


@pytest.fixture
def return_valid_django_backend_models_to_ignore():
    return valid_django_backend_models_to_ignore


@pytest.fixture
def return_valid_django_backend_to_ts_conversions():
    return valid_django_backend_to_ts_conversions


# MARK: Invalid

# invalid_django_models
invalid_django_models = config["invalid_django_model"]["backend_model_path"]
invalid_django_ts_interfaces = [
    Path(p) for p in config["invalid_django_model"]["ts_interface_paths"]
]
invalid_django_check_blank_models = config["invalid_django_model"][
    "check_blank_model_fields"
]
invalid_django_backend_models_to_ignore = config["invalid_django_model"][
    "backend_models_to_ignore"
]
invalid_django_backend_to_ts_conversions = config["invalid_django_model"][
    "backend_to_ts_model_name_conversions"
]

# invalid_fastapi_models
invalid_fastapi_models = config["invalid_fastapi_model"]["backend_model_path"]
invalid_fastapi_ts_interfaces = [
    Path(p) for p in config["invalid_fastapi_model"]["ts_interface_paths"]
]
invalid_fastapi_check_blank_models = config["invalid_fastapi_model"][
    "check_blank_model_fields"
]
invalid_fastapi_backend_models_to_ignore = config["invalid_fastapi_model"][
    "backend_models_to_ignore"
]
invalid_fastapi_backend_to_ts_conversions = config["invalid_fastapi_model"][
    "backend_to_ts_model_name_conversions"
]


# django fixtures
@pytest.fixture
def return_invalid_django_models():
    return str(invalid_django_models)


@pytest.fixture
def return_invalid_django_concatenated_types_file():
    concatenated_types_file = ""
    for p in invalid_django_ts_interfaces:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    return concatenated_types_file


@pytest.fixture
def return_invalid_django_check_blank_models():
    return invalid_django_check_blank_models


@pytest.fixture
def return_invalid_django_backend_models_to_ignore():
    return invalid_django_backend_models_to_ignore


@pytest.fixture
def return_invalid_django_backend_to_ts_conversions():
    return invalid_django_backend_to_ts_conversions


# invalid fastapi_models
@pytest.fixture
def return_invalid_fastapi_models():
    return str(invalid_fastapi_models)


@pytest.fixture
def return_invalid_fastapi_concatenated_types_file():
    concatenated_types_file = ""
    for p in invalid_fastapi_ts_interfaces:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    return concatenated_types_file


@pytest.fixture
def return_invalid_fastapi_check_blank_models():
    return invalid_fastapi_check_blank_models


@pytest.fixture
def return_invalid_fastapi_backend_models_to_ignore():
    return invalid_fastapi_backend_models_to_ignore


@pytest.fixture
def return_invalid_fastapi_backend_to_ts_conversions():
    return invalid_fastapi_backend_to_ts_conversions


@pytest.fixture
def parser():
    """A MinimalParser instance with no ignore list."""
    return MinimalParser()


# MARK: ABC Contract


def test_backend_model_parser_is_abstract():
    with pytest.raises(TypeError):
        BackendModelParser()


def test_cannot_instantiate_without_implementing_build_models():
    class IncompleteParser(BackendModelParser):
        pass

    with pytest.raises(TypeError):
        IncompleteParser()


def test_can_initiate_when_build_models_is_implemented():
    assert isinstance(parser, BackendModelParser)


def test_build_models_signature_accepts_expected_arguments(parser):
    result = parser._build_models(
        direct_fields={}, direct_blank_fields={}, inherited={}, model_lines={}
    )
    assert isinstance(result, ModelData)
