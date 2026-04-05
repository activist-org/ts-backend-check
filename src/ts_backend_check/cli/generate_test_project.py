# SPDX-License-Identifier: GPL-3.0-or-later
"""
Functionality to copy the test project files from the package to the present working directory.
"""

import os
import shutil
from pathlib import Path

# Check for Windows and derive directory path separator.
PATH_SEPARATOR = "\\" if os.name == "nt" else "/"
INTERNAL_TEST_PROJECT_DIR_PATH = Path(__file__).parent.parent / "test_project"


def get_test_project_config_file_text() -> str:
    """
    Return the text for the configuration file for the ts-backend-check test project.

    Returns
    -------
    str
        The text for the configuration file for the ts-backend-check test project.
    """

    return """# Configuration file for ts-backend-check validation.
# See https://github.com/activist-org/ts-backend-check for details.

valid_model:
  backend_model_path: src/ts_backend_check/test_project/backend/models.py
  ts_interface_paths:
    - src/ts_backend_check/test_project/frontend/valid_interfaces_1.ts
    - src/ts_backend_check/test_project/frontend/valid_interfaces_2.ts
  check_blank_model_fields: true
  backend_models_to_ignore:
    - BackendOnlyModel
  backend_to_ts_model_name_conversions:
    EventModel:
      - Event
      - EventExtended
    UserModel:
      - User

invalid_model:
  backend_model_path: src/ts_backend_check/test_project/backend/models.py
  ts_interface_paths:
    - src/ts_backend_check/test_project/frontend/invalid_interfaces.ts
  check_blank_model_fields: true
  backend_to_ts_model_name_conversions:
    EventModel:
      - Event
      - EventExtended
    # UserModel:
    #   - User
"""


def write_test_project_config_file(config_file_name: str) -> None:
    """
    Write a YAML configuration file for the ts-backend-check test project.

    Parameters
    ----------
    config_file_name : str
        The name for the ts-backend-check configuration file.

    Returns
    -------
    None
        The contents of a configuration file are written to match the test project.
    """
    test_project_config = get_test_project_config_file_text()
    with open(config_file_name, "w") as file:
        file.write(test_project_config)


def generate_test_project() -> None:
    """
    Copy the ts_backend_check/test_project directory to the present working directory.
    """
    if not Path("./ts_backend_check_test_project/").is_dir():
        print(
            f"Generating testing project for ts-backend-check in .{PATH_SEPARATOR}ts_backend_check_test_project{PATH_SEPARATOR} ..."
        )

        shutil.copytree(
            INTERNAL_TEST_PROJECT_DIR_PATH,
            Path("./ts_backend_check_test_project/"),
            dirs_exist_ok=True,
        )

        print("The test project has been successfully generated.")
        print(
            "Within the test project there's one model interface identifier that passes all checks and one that fails all checks."
        )

        if (
            not Path(".ts-backend-check.yaml").is_file()
            and not Path(".ts-backend-check.yml").is_file()
        ):
            print("No .ts-backend-check.yaml configuration file found.")

            generate_test_project_config_answer = None
            while generate_test_project_config_answer not in ["y", "n", ""]:
                generate_test_project_config_answer = (
                    input(
                        "Would you like to generate a configuration file for the test project? ([y]/n): "
                    )
                    .strip()
                    .lower()
                )

            if generate_test_project_config_answer in ["y", ""]:
                write_test_project_config_file(
                    config_file_name=".ts-backend-check.yaml"
                )
                print(
                    "A .ts-backend-check.yaml configuration file has been written to match the test project."
                )

        else:
            config_file_name = (
                ".ts-backend-check.yaml"
                if Path(".ts-backend-check.yaml").is_file()
                else ".ts-backend-check.yml"
            )
            generate_test_project_config_answer = None
            while generate_test_project_config_answer not in ["y", "n", ""]:
                generate_test_project_config_answer = (
                    input(
                        f"Would you like to overwrite the {config_file_name} configuration file for the test project? ([y]/n): "
                    )
                    .strip()
                    .lower()
                )

            if generate_test_project_config_answer in ["y", ""]:
                write_test_project_config_file(
                    config_file_name=".ts-backend-check.yaml"
                )
                print(
                    f"The {config_file_name} configuration file has been overwritten to match the test project."
                )

            else:
                print(
                    f"You can set which models and interfaces to test in the {config_file_name} configuration file."
                )

    else:
        print(
            f"Test project for ts-backend-check already exist in .{PATH_SEPARATOR}ts_backend_check_test_project{PATH_SEPARATOR} and will not be regenerated."
        )
