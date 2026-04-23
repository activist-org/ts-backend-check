# SPDX-License-Identifier: GPL-3.0-or-later
"""
Configure cli to run based on a YAML configuration file.
"""

from pathlib import Path
from typing import Any, Dict

from rich import print as rprint
from yaml import dump, safe_load

from ts_backend_check.utils import get_config_file_path

CWD_PATH = Path.cwd()
YAML_CONFIG_FILE_PATH = get_config_file_path()


def path_exists(path: str) -> bool:
    """
    Check if path entered by the user exists withing the filesystem.

    Parameters
    ----------
    path : str
        Path should be entered as a string from the user.

    Returns
    -------
    bool
        Return true or false based on if path exists.
    """
    full_path = Path.cwd() / path
    return bool(Path(full_path).is_file())


def config_file_is_valid() -> bool:
    """
    Check that the configuration file for ts-backend-check is not empty and has the necessary keys.

    Returns
    -------
    bool
        True if the ts-backend-check configuration file is valid. False otherwise.
    """
    with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config = safe_load(file)

        if config is not None:
            for i in config.keys():
                if not isinstance(config[i], dict):
                    rprint(
                        f"[red]The ts-backend-check identifier '{i}' in the configuration file is not a dictionary. Please check the configuration file and try again.[/red]"
                    )
                    return False

                if config[i]["backend_model_path"] is None:
                    rprint(
                        f"[red]The ts-backend-check identifier '{i}' in the configuration file does not have a backend_model_path argument. Please check the configuration file and try again.[/red]"
                    )
                    return False

                if config[i]["ts_interface_paths"] is None:
                    rprint(
                        f"[red]The ts-backend-check identifier '{i}' in the configuration file does not have a ts_interface_paths argument. Please check the configuration file and try again.[/red]"
                    )
                    return False

            return True

        else:
            rprint(
                "[red]The ts-backend-check configuration file is empty. Please regenerate your config file with tsbc -gcf.[/red]"
            )
            return False


def write_config(config: dict[str, dict[str, object]]) -> None:
    """
    Function to write into .ts-backend-check.yaml file.

    Parameters
    ----------
    config : dict[str, dict[str, object]]
        Passing a dictionary as key str with another dict as value.
    """
    try:
        options = f"""# Configuration file for ts-backend-check validation.
# See https://github.com/activist-org/ts-backend-check for details.

{dump(config, sort_keys=False)}"""

        with open(YAML_CONFIG_FILE_PATH, "w") as file:
            file.write(options)

    except IOError as e:
        print(f"Error while writing configuration file: {e}")


def configure_model_interface_arguments() -> None:
    """
    Function to receive paths from user.
    """
    config_options: Dict[str, Any] = {}
    while True:
        print(
            "\nAdding new model-interface configuration. Please provide the information as directed:"
        )

        key = input(
            "Enter a model-interface identifier (eg: auth, user, event): "
        ).strip()
        if not key:
            rprint(
                "\n[red]The model-interface identifier cannot be empty. Please try again.[/red]"
            )
            continue

        # Get backend path.
        while True:
            backend_path = input("Enter the path for Django models.py file: ").strip()
            if not backend_path:
                rprint(
                    "[red]The path for the Django models.py file cannot be empty. Please try again.[/red]"
                )
                continue

            if path_exists(backend_path):
                break

            rprint(f"[red]File not found: {CWD_PATH / backend_path}[/red]")
            rprint("[yellow]Please check the path and try again.[/yellow]")

        # Get frontend path.
        while True:
            frontend_path = input(
                "Enter the path to TypeScript interface file: "
            ).strip()
            if not frontend_path:
                rprint(
                    "[red]The path for the TypeScript interface file cannot be empty. Please try again.[/red]"
                )
                continue

            if path_exists(frontend_path):
                break

            rprint(f"[red]File not found: {CWD_PATH / frontend_path}[/red]")
            rprint("[yellow]Please check the path and try again.[/yellow]")

        # Get whether to check blank model fields.
        while True:
            check_blank_model_fields_response = (
                input(
                    "The check should assert that model fields that can be blank must also be optional in interfaces ([y]/n): "
                )
                .strip()
                .lower()
            )

            if check_blank_model_fields_response in ["y", ""]:
                check_blank_model_fields = True
                break

            elif check_blank_model_fields_response == "n":
                check_blank_model_fields = False
                break

            else:
                rprint("[red]Invalid response. Please try again.[/red]")

        # Get Backend models to ignore.
        backend_models_to_ignore: list[str] = []
        confirm_backend_models_to_ignore = (
            input(
                "Are there backend models that should be ignored as they don't have frontend interfaces? (y/[n])"
            )
            .strip()
            .lower()
        )

        while True:
            if confirm_backend_models_to_ignore in ["n", ""]:
                break

            model = input("Enter name of the model to ignore: ").strip()
            backend_models_to_ignore.append(model)
            confirm_continue = input("Add another model to ignore: ").strip().lower()
            if confirm_continue in ["n", ""]:
                break

        # Get model name conversions.
        rprint(
            "[yellow]💡 Note: You need model name conversions if your TypeScript interfaces are not named exactly the same as the corresponding models (i.e. UserModel in Django and User in TS).[/yellow]"
        )

        backend_to_ts_model_name_conversions: Dict[str, list[str]] = {}
        while True:
            name_conversions_needed = (
                input("Model name conversions are needed (y/[n]): ").strip().lower()
            )

            if name_conversions_needed in ["n", ""]:
                break

            while True:
                while True:
                    if backend_model_name := input(
                        "Enter the backend model name: "
                    ).strip():
                        break

                    else:
                        rprint("[red]Invalid response. Please try again.[/red]")

                while True:
                    if ts_interface_name := [
                        name.strip()
                        for name in input(
                            "Enter the TypeScript interface name (if multiple separate them with commas): "
                        ).split(",")
                    ]:
                        break

                    else:
                        rprint("[red]Invalid response. Please try again.[/red]")

                backend_to_ts_model_name_conversions[backend_model_name] = (
                    ts_interface_name
                )

                further_name_conversions_needed = (
                    input("Add more model name conversions (y/[n]): ").strip().lower()
                )
                if further_name_conversions_needed in ["n", ""]:
                    break

            break

        config_options[key] = {
            "backend_model_path": backend_path,
            "ts_interface_paths": frontend_path,
            "check_blank_model_fields": check_blank_model_fields,
            "backend_models_to_ignore": backend_models_to_ignore
            if len(backend_models_to_ignore) > 0
            else None,
        }

        if backend_to_ts_model_name_conversions:
            config_options[key]["backend_to_ts_model_name_conversions"] = (
                backend_to_ts_model_name_conversions
            )

        write_config(config_options)
        rprint(f"[green]✅ Added configuration for the '{key}' check.[/green]")

        continue_config = input(
            "Add another model-interface configuration (y/[n]): "
        ).strip()

        if continue_config.lower() in ["n", ""]:
            if config_options:
                optional_s = "s" if len(config_options) > 1 else ""
                rprint(
                    f"[green]✅ Configuration complete! Added {len(config_options)} configuration{optional_s} to check.[/green]"
                )
            break


def generate_config_file() -> None:
    """
    Main function to create or update configuration.
    """
    header = "ts-backend-check Configuration Setup"
    print(header)
    print("=" * len(header))

    if YAML_CONFIG_FILE_PATH.is_file():
        reconfigure_choice = input(
            "Configuration file exists. Confirm if you want to re-configure your .ts-backend-check.yaml file (y/[n]): "
        )
        if reconfigure_choice.lower() in ["n", ""]:
            print("Exiting without changes.")
            return

        print("Reconfiguring...")

    else:
        print("Creating new configuration file...")

    try:
        configure_model_interface_arguments()

    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled by user.")

    except Exception as e:
        print(f"\nError during configuration: {e}")
        print("Configuration cancelled.")
