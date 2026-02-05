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
            "Within the project there's one model that passes all checks and one that fails all checks."
        )
        if (
            not Path(".ts-backend-check.yaml").is_file()
            and not Path(".ts-backend-check.yml").is_file()
        ):
            print(
                "You can set which one to test in an ts-backend-check configuration file."
            )
            print(
                "Please generate one with the 'ts-backend-check --generate-config-file' command."
            )

        elif Path(".ts-backend-check.yaml").is_file():
            print("You can set which one to test in the .ts-backend-check.yaml file.")

        elif Path(".ts-backend-check.yml").is_file():
            print("You can set which one to test in the .ts-backend-check.yml file.")

    else:
        print(
            f"Test project for ts-backend-check already exist in .{PATH_SEPARATOR}ts_backend_check_test_project{PATH_SEPARATOR} and will not be regenerated."
        )
