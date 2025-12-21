# SPDX-License-Identifier: GPL-3.0-or-later
"""
Configure cli to run based on a YAML configuration file.
"""

from pathlib import Path

from yaml import dump

YAML_CONFIG_FILE_PATH = (
    Path(__file__).parent.parent.parent.parent / ".ts-backend-check.yaml"
)

PROJECT_ROOT_PATH = Path(__file__).parent.parent.parent.parent


def configure_paths() -> None:
    """
    Function to receive paths from user.
    """
    config_options = {}
    while True:
        print("\n--- Adding new model/interface configuration ---")

        key = input(
            "Enter the model-interface type (eg: 'auth', 'orgs', 'groups'): "
        ).strip()
        if not key:
            print("Key cannot be empty. Please try again.")
            continue

        # Get backend path.
        while True:
            backend_path = input("Enter the path for Django models.py file: ").strip()
            if not backend_path:
                print("Path cannot be empty.")
                continue

            if path_exists(backend_path):
                break

            print(f"File not found: {PROJECT_ROOT_PATH / backend_path}")
            print("Please check the path and try again.")

        # Get frontend path.
        while True:
            frontend_path = input("Enter path to TypeScript interface file: ").strip()
            if not frontend_path:
                print("Path cannot be empty. Please try again.")
                continue

            if path_exists(frontend_path):
                break

            print(f"File not found: {PROJECT_ROOT_PATH / frontend_path}")
            print("Please check the path and try again.")

        config_options[key] = {
            "backend_model_path": backend_path,
            "frontend_interface_path": frontend_path,
        }

        print(f"✓ Added configuration for '{key}'")

        continue_config = input(
            "Do you wish to add another model/interface configuration? (y/[n])"
        ).strip()

        if continue_config.lower() in ["n", ""]:
            if config_options:
                write_config(config_options)
                print(
                    f"\n✓ Configuration complete! Added {len(config_options)} configuration(s)."
                )
            break

        if config_options:
            write_config(config_options)
            print(
                f"\n✓ Configuration complete! Added {len(config_options)} configuration(s)."
            )

        else:
            print("\nNo configurations added.")


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
    full_path = Path(__file__).parent.parent.parent.parent / path
    if Path(full_path).is_file():
        return True

    return False


def write_config(config: dict[str, dict[str, str]]) -> None:
    """
    Function to write into .ts-backend-check.yaml file.

    Parameters
    ----------
    config : dict[str, dict[str, str]]
        Passing a dictionary as key str with another dict as value.
    """
    try:
        options = f"""# Configuration file for ts-backend-check validation.
# See https://github.com/activist-org/ts-backend-check for details.

# Paths:
{dump(config)}

"""
        with open(YAML_CONFIG_FILE_PATH, "w") as file:
            file.write(options)

    except IOError as e:
        print(f"Error while writing config file: {e}")


def create_config() -> None:
    """
    Main function to create or update configuration.
    """
    print("ts-backend-check Configuration Setup")
    print("=" * 40)

    if YAML_CONFIG_FILE_PATH.is_file():
        reconfig_choice = input(
            "Configuration file exists. Do you want to re-configure your .ts-backend-check.yaml file? (y/[n]) "
        )
        if reconfig_choice.lower() in ["n", ""]:
            print("Exiting without changes.")
            return

        print("Reconfiguring...")

    else:
        print("Creating new configuration file...")

    try:
        configure_paths()

    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled by user.")

    except Exception as e:
        print(f"\nError during configuration: {e}")
        print("Configuration cancelled.")


if __name__ == "__main__":
    create_config()
