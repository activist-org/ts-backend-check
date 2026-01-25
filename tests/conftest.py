# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from ts_backend_check.cli.main import config

invalid_django_models = config["invalid_model"]["backend_model_path"]
invalid_ts_interfaces = config["invalid_model"]["ts_interface_path"]


@pytest.fixture
def return_invalid_django_models():
    return str(invalid_django_models)


@pytest.fixture
def return_invalid_ts_interfaces():
    return str(invalid_ts_interfaces)


valid_django_models = config["valid_model"]["backend_model_path"]
valid_ts_interfaces = config["valid_model"]["ts_interface_path"]


@pytest.fixture
def return_valid_django_models():
    return str(valid_django_models)


@pytest.fixture
def return_valid_ts_interfaces():
    return str(valid_ts_interfaces)
