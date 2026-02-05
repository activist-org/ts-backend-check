# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from ts_backend_check.cli.main import config

# MARK: Invalid

invalid_django_models = config["invalid_model"]["backend_model_path"]
invalid_ts_interfaces = config["invalid_model"]["ts_interface_path"]
invalid_check_blank_models = config["invalid_model"]["check_blank_model_fields"]


@pytest.fixture
def return_invalid_django_models():
    return str(invalid_django_models)


@pytest.fixture
def return_invalid_ts_interfaces():
    return str(invalid_ts_interfaces)


@pytest.fixture
def return_invalid_check_blank_models():
    return invalid_check_blank_models


# MARK: Valid

valid_django_models = config["valid_model"]["backend_model_path"]
valid_ts_interfaces = config["valid_model"]["ts_interface_path"]
valid_check_blank_models = config["valid_model"]["check_blank_model_fields"]
valid_backend_to_ts_conversions = config["valid_model"][
    "backend_to_ts_model_name_conversions"
]


@pytest.fixture
def return_valid_django_models():
    return str(valid_django_models)


@pytest.fixture
def return_valid_ts_interfaces():
    return str(valid_ts_interfaces)


@pytest.fixture
def return_valid_check_blank_models():
    return valid_check_blank_models


@pytest.fixture
def return_valid_backend_to_ts_conversions():
    return valid_backend_to_ts_conversions
