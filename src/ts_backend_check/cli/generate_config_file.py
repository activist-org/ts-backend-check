# SPDX-License-Identifier: GPL-3.0-or-later
"""
Configure cli to run based on a YAML configuration file.
"""

from pathlib import Path
from typing import Any

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


def prompt_yes_no(prompt: str) -> bool:
    """
    Prompt the user and receive a yes or no input.

    Parameters
    ----------
    prompt : str
        Prompt question to receive str input.

    Returns
    -------
    bool
        Return the boolean value.
    """
    while True:
        response = input(prompt).strip().lower()

        if "([y]/n)" in prompt:
            if response in ("y", ""):
                return True

            elif response == "n":
                return False

        if "(y/[n])" in prompt:
            if response == "y":
                return True

            if response in ("n", ""):
                return False

        rprint("[red]Invalid response. Please try again.[/red]")


def config_file_validation(config: dict) -> bool:
    """
    Validate the configuration file for ts-backend-check to ensure it has the necessary keys, values and types.

    Parameters
    ----------
    config : dict
        The configuration file to validate.

    Returns
    -------
    bool
        True if the configuration file is valid. False otherwise.
    """
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
        return config_file_validation(config)


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


def get_file_path_from_user(
    description: str | None,
    input_prompt: str,
    no_key_description: str,
) -> str | None:
    """
    Function to prompt the user about file Path.

    Parameters
    ----------
    description : str | None
        Description to prompt the user.

    input_prompt : str
        Specified prompt for receiving input paths.

    no_key_description : str
        Prompt the user when file path is not found.

    Returns
    -------
    str | None
        Return the path when its found otherwise None.
    """
    if description is not None:
        print(description)

    key: str = input(input_prompt).strip()
    if not key:
        rprint(no_key_description)
        return None

    return key


def collect_and_validated_backend_model_path() -> str:
    """
    Prompt the user for the file path.

    Returns
    -------
    str
        Return the path once it's found.
    """
    while True:
        path = get_file_path_from_user(
            description=None,
            input_prompt="Enter the path for the Django models.py file: ",
            no_key_description="[red]The path for the Django models.py file cannot be empty. Please try again.[/red]",
        )
        if not path:
            continue

        if path_exists(path):
            return path

        rprint(f"[red]File not found: {CWD_PATH / path}[/red]")
        rprint("[yellow]Please check the path and try again.[/yellow]")


def collect_and_validate_frontend_interface_paths() -> list[str]:
    """
    Collect the frontend paths and validate their existence.

    Returns
    -------
    list[str]
        Return frontend paths in list[str].
    """
    paths: list[str] = []
    while True:
        path = get_file_path_from_user(
            description=None,
            input_prompt="Enter the path to a TypeScript interface file: ",
            no_key_description="[red]The path for the TypeScript interface file cannot be empty. Please try again.[/red]",
        )
        if not path:
            continue

        if not path_exists(path):
            rprint(f"[red]File not found: {CWD_PATH / path}[/red]")
            rprint("[yellow]Please check the path and try again.[/yellow]")
            continue

        paths.append(path)
        if input(
            "Do you want to continue to add more TypeScript interface file paths? (y/[n]): "
        ) in ("n", ""):
            return paths


def collect_backend_models_to_ignore() -> list[str]:
    """
    Collect the names of backend models that should be ignored.

    Returns
    -------
    list[str]
        A list of Models needs to be ignored.
    """
    if not prompt_yes_no(
        prompt="Are there backend models that should be ignored? (y/[n]): ",
    ):
        return []

    models: list[str] = []
    while True:
        models.append(input("Enter name of the model to ignore: ").strip())
        if not prompt_yes_no(
            prompt="Add another model to ignore (y/[n]): ",
        ):
            return models


def collect_model_name_conversions() -> dict[str, list[str]]:
    """
    Collect model names that should be converted.

    Returns
    -------
    dict[str,list[str]]
        A dictionary of converted models after input Prompts.
    """
    rprint(
        "[yellow]💡 Note: You need model name conversions if your TypeScript interfaces are not named exactly the same as the corresponding models (i.e. UserModel in Django and User in TS).[/yellow]"
    )
    conversions: dict[str, list[str]] = {}
    if not prompt_yes_no(
        prompt="Model name conversions are needed (y/[n]): ",
    ):
        return conversions

    while True:
        while not (backend_name := input("Enter the backend model name: ").strip()):
            rprint("[red]Invalid response. Please try again.[/red]")

        ts_names = [
            n.strip()
            for n in input(
                "Enter the TypeScript interface name(s) (comma-separated): "
            ).split(",")
        ]
        conversions[backend_name] = ts_names
        if not prompt_yes_no(
            prompt="Add more model name conversions (y/[n]): ",
        ):
            return conversions


def derive_entry(
    backend_model_path: str,
    ts_interface_paths: list[str],
    check_blank_model_fields: bool,
    backend_models_to_ignore: list | None,
) -> dict[str, Any]:
    """
    Derive a configuration file entry dictionary from component parts.

    Parameters
    ----------
    backend_model_path : str
        The backend model path for the configuration entry.

    ts_interface_paths : list[str]
        The list of frontend interface file paths for the configuration entry.

    check_blank_model_fields :  bool
        The boolean value for whether blank model fields should be checked.

    backend_models_to_ignore : list | None
        The list of backend models to ignore.

    Returns
    -------
    dict[str,Any]
        A dictionary consisting of Various paths and values.
    """
    entry: dict[str, Any] = {
        "backend_model_path": backend_model_path,
        "ts_interface_paths": ts_interface_paths,
        "check_blank_model_fields": check_blank_model_fields,
        "backend_models_to_ignore": backend_models_to_ignore,
    }
    return entry


def configure_model_interface_entries() -> None:
    """
    Prompt the user for arguments that should be used to create the configuration file entries.
    """
    config_options: dict[str, Any] = {}
    while True:
        key = get_file_path_from_user(
            description="\nAdding new model-interface configuration. Please provide the information as directed:",
            input_prompt="Enter a model-interface identifier (eg: auth, user, event): ",
            no_key_description="\n[red]The model-interface identifier cannot be empty. Please try again.[/red]",
        )
        if not key:
            continue

        backend_model_path = collect_and_validated_backend_model_path()
        ts_interface_paths = collect_and_validate_frontend_interface_paths()
        check_blank_model_fields = prompt_yes_no(
            "Assert that blank model fields must also be optional in interfaces ([y]/n): ",
        )
        backend_models_to_ignore = collect_backend_models_to_ignore()
        model_name_conversions = collect_model_name_conversions()

        entry: dict[str, Any] = derive_entry(
            backend_model_path=backend_model_path,
            ts_interface_paths=ts_interface_paths,
            check_blank_model_fields=check_blank_model_fields,
            backend_models_to_ignore=backend_models_to_ignore,
        )
        if model_name_conversions:
            entry["backend_to_ts_model_name_conversions"] = model_name_conversions

        config_options[key] = entry
        write_config(config_options)
        rprint(f"[green]✅ Added configuration for the '{key}' check.[/green]")

        if not prompt_yes_no("Add another model-interface configuration (y/[n]): "):
            optional_s = "s" if len(config_options) > 1 else ""
            rprint(
                f"[green]✅ Configuration complete! Added {len(config_options)} configuration{optional_s} to check.[/green]"
            )
            break

        if not prompt_yes_no(
            prompt="Add another model-interface configuration (y/[n]): "
        ):
            break

    if config_options:
        optional_s = "s" if len(config_options) > 1 else ""
        rprint(
            f"[green]✅ Configuration complete! Added {len(config_options)} configuration{optional_s} to check.[/green]"
        )


def generate_config_file() -> None:
    """
    Main function to create or update configuration.
    """
    header = "ts-backend-check Configuration Setup"
    print(header)
    print("=" * len(header))

    if YAML_CONFIG_FILE_PATH.is_file():
        if not prompt_yes_no(
            prompt="Configuration file exists. Confirm if you want to re-configure your .ts-backend-check.yaml file (y/[n]): "
        ):
            print("Exiting without changes.")
            return

        print("Reconfiguring...")

    else:
        print("Creating new configuration file...")

    try:
        configure_model_interface_entries()

    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled by user.")

    except Exception as e:
        print(f"\nError during configuration: {e}")
        print("Configuration cancelled.")
