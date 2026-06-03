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


def prompt_validated_path(input_description: str, empty_error: str) -> str:
    """
    Prompt the user for the file path.

    Parameters
    ----------
    input_description : str
        Specified description for receiving input paths.

    empty_error : str
        Prompt the user when file path is not found.

    Returns
    -------
    str
        Return the path once it's found.
    """
    while True:
        path = get_file_path_from_user(
            description=None,
            input_prompt=input_description,
            no_key_description=empty_error,
        )
        if not path:
            continue
        if path_exists(path):
            return path
        rprint(f"[red]File not found: {CWD_PATH / path}[/red]")
        rprint("[yellow]Please check the path and try again.[/yellow]")


def collect_frontend_paths() -> list[str]:
    """
    Collect the frontend paths.

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


def prompt_yes_no(prompt: str, default_yes: bool = True) -> bool:
    """
    Function to Prompt the user and receive Yes or No input.

    Parameters
    ----------
    prompt : str
        Prompt a question to receive str input.

    default_yes : bool
        Boolean value for default yes inputs.

    Returns
    -------
    bool
        Return the boolean value.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ("y", "") and default_yes:
            return True
        if response == "n":
            return False
        if response == "y":
            return True
        rprint("[red]Invalid response. Please try again.[/red]")


def collect_models_to_ignore() -> list[str]:
    """
    Function to collect and ignore models.

    Returns
    -------
    list[str]
        A list of Models needs to be ignored.
    """
    if input(
        "Are there backend models that should be ignored? (y/[n]): "
    ).strip().lower() in ("n", ""):
        return []
    models: list[str] = []
    while True:
        models.append(input("Enter name of the model to ignore: ").strip())
        if input("Add another model to ignore [y/[n]]").strip().lower() in ("n", ""):
            return models


def collect_model_name_conversions() -> dict[str, list[str]]:
    """
    Function to collect model names which are conversed.

    Returns
    -------
    dict[str,list[str]]
        A dictionary of conversed models after input Prompts.
    """
    rprint(
        "[yellow]💡 Note: You need model name conversions if your TypeScript interfaces are not named exactly the same as the corresponding models (i.e. UserModel in Django and User in TS).[/yellow]"
    )
    conversions: dict[str, list[str]] = {}
    if input("Model name conversions are needed (y/[n]): ").strip().lower() in (
        "n",
        "",
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
        if input("Add more model name conversions (y/[n]): ").strip().lower() in (
            "n",
            "",
        ):
            return conversions


def continue_add_config(prompt: str) -> bool:
    """
    Function to get Required prompts.

    Parameters
    ----------
    prompt : str
        Get Prompt as an input.

    Returns
    -------
    bool
        Returns Boolean Value.
    """
    continue_config = prompt_yes_no(prompt=prompt)
    return continue_config


def create_entry(
    backend_path: str,
    frontend_path_lists: list[str],
    check_blank_model_fields: bool,
    backend_models_to_ignore: list | None,
) -> dict[str, Any]:
    """
    Function to create a entry dictionary.

    Parameters
    ----------
    backend_path : str
        Get Backend Path.

    frontend_path_lists : list[str]
        Get a list of Frontend Paths.

    check_blank_model_fields :  bool
        Get the boolean value for blank_model_fields.

    backend_models_to_ignore : list | None
        Get the backend models to ignore.

    Returns
    -------
    dict[str,Any]
        A dictionary consisting of Various paths and values.
    """
    entry: dict[str, Any] = {
        "backend_model_path": backend_path,
        "ts_interface_paths": frontend_path_lists,
        "check_blank_model_fields": check_blank_model_fields,
        "backend_models_to_ignore": backend_models_to_ignore,
    }
    return entry


def configure_model_interface_arguments() -> None:
    """
    Function to receive paths from user.
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

        # Get backend path.
        backend_path = prompt_validated_path(
            input_description="Enter the path for the Django models.py file: ",
            empty_error="[red]The path for the Django models.py file cannot be empty. Please try again.[/red]",
        )
        # Get frontend paths.
        frontend_path_lists = collect_frontend_paths()
        # Get whether to check blank model fields.
        check_blank_model_fields = prompt_yes_no(
            "Assert that blank model fields must also be optional in interfaces ([y]/n): "
        )
        # models to ignore
        backend_models_to_ignore = collect_models_to_ignore()
        # model name conversions
        model_name_conversions = collect_model_name_conversions()

        entry: dict[str, Any] = create_entry(
            backend_path,
            frontend_path_lists,
            check_blank_model_fields,
            backend_models_to_ignore,
        )
        if model_name_conversions:
            entry["backend_to_ts_model_name_conversions"] = model_name_conversions

        config_options[key] = entry
        write_config(config_options)
        rprint(f"[green]✅ Added configuration for the '{key}' check.[/green]")

        if input(
            "Add another model-interface configuration (y/[n]): "
        ).strip().lower() in ("n", ""):
            optional_s = "s" if len(config_options) > 1 else ""
            rprint(
                f"[green]✅ Configuration complete! Added {len(config_options)} configuration{optional_s} to check.[/green]"
            )
            break

        if not continue_add_config(
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
