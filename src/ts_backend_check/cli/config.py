# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from yaml import dump

YAML_CONFIG_FILE_PATH = (
    Path(__file__).parent.parent.parent.parent / ".ts-backend-check.yaml"
)

config_options = {}


def path_exits(path: str) -> bool:
    full_path = Path(__file__).parent.parent.parent.parent / path
    if Path(full_path).is_file():
        return True
    return False


def write_config(config: dict[str, dict[str, str]]) -> None:
    options = f"""
# Configuration file for ts-backend-check validation.
# See https://github.com/activist-org/ts-backend-check for details.

# Paths:
{dump(config)}

"""
    with open(YAML_CONFIG_FILE_PATH, "w") as file:
        file.write(options)
    return None


def create_config() -> None:
    if YAML_CONFIG_FILE_PATH.is_file():
        reconfig_choice = input(
            "Config exists. Do you want to re-configure your config.yaml file? "
        )
        if reconfig_choice.lower() == "y":
            while_cond = True
            while while_cond:
                if reconfig_choice.lower() == "y":
                    key = input(
                        "Enter the model/interface type (ex: auth models/interface, org models/interface): "
                    )
                    backend_model_path = input("Enter path to Django models.py file: ")
                    frontend_interface_path = input(
                        "Enter path to TypeScript interface file: "
                    )
                    if path_exits(backend_model_path) and path_exits(
                        frontend_interface_path
                    ):
                        config_options[key] = {
                            "backend_model_path": backend_model_path,
                            "frontend_interface_path": frontend_interface_path,
                        }
                        loop_end = input(
                            "Continue entering paths to other models-interface? "
                        )
                        print("\n")
                        if loop_end.lower() == "n":
                            while_cond = False
                    else:
                        print(
                            "Check the paths entered, one or more file does not exist in the given path."
                        )

            write_config(config_options)
        else:
            print("Exiting.")

    else:
        print(
            "Creating a new .ts-backend-check.yaml file in the root dir. Run ts-backend-check --configure to configure your checks."
        )
        open(YAML_CONFIG_FILE_PATH, "w").close()


if __name__ == "__main__":
    create_config()
