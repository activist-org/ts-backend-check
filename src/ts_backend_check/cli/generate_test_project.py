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
  backend_models_to_ignore:
    - BackendOnlyModel
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
    test_project_config_text = get_test_project_config_file_text()
    with open(config_file_name, "w") as file:
        file.write(test_project_config_text)


def check_and_generate_yaml_config_file_for_test_project(yaml_files: list[str]) -> None:
    """
    Generate a .yaml configuration file if it does not exist in the present working directory.

    Parameters
    ----------
    yaml_files : list[str]
        Receives a list of the two possible .yaml configuration file as strings.

    Returns
    -------
    None
        The User gets prompted to generate a configuration file for the test project.
    """
    file1, file2 = yaml_files
    if not Path(file1).is_file() and not Path(file2).is_file():
        print(f"No {file1} configuration file found.")

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
            write_test_project_config_file(config_file_name=file1)
            print(
                f"A {file1} configuration file has been written to match the test project."
            )
    else:
        config_file_name = file1 if Path(file1).is_file() else file2
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
            write_test_project_config_file(config_file_name=config_file_name)
            print(
                f"The {config_file_name} configuration file has been overwritten to match the test project."
            )

        else:
            print(
                f"You can set which models and interfaces to test in the {config_file_name} configuration file."
            )


def generate_test_project() -> None:
    """
    Copy the ts_backend_check/test_project directory to the present working directory.
    """
    yaml_files: list[str] = [".ts-backend-check.yaml", ".ts-backend-check.yml"]
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
            "Within the test project there's one model-interface identifier that passes all checks and one that fails all checks."
        )

        check_and_generate_yaml_config_file_for_test_project(yaml_files=yaml_files)
    else:
        print(
            f"Test project for ts-backend-check already exist in .{PATH_SEPARATOR}ts_backend_check_test_project{PATH_SEPARATOR} and will not be regenerated."
        )
