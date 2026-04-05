# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the ts-backend-check command line interface.
"""

import argparse
import sys
from argparse import ArgumentParser
from pathlib import Path

import yaml
from rich import print as rprint
from rich.text import Text

from ts_backend_check.checker import TypeChecker
from ts_backend_check.cli.generate_config_file import generate_config_file
from ts_backend_check.cli.generate_test_project import generate_test_project
from ts_backend_check.cli.upgrade import upgrade_cli
from ts_backend_check.cli.version import get_version_message

# MARK: Base Paths

CWD_PATH = Path.cwd()


def get_config_file_path() -> Path:
    """
    Get the path to the ts-backend-check configuration file.

    Checks for both .yaml and .yml extensions, preferring .yaml if both exist.

    Returns
    -------
    Path
        The path to the configuration file (.yaml or .yml).
    """
    yaml_path = CWD_PATH / ".ts-backend-check.yaml"
    yml_path = CWD_PATH / ".ts-backend-check.yml"

    # Prefer .yaml if it exists, otherwise check for .yml.
    if yaml_path.is_file():
        return yaml_path

    elif yml_path.is_file():
        return yml_path

    else:
        # Default to .yaml for new files.
        return yaml_path


def check_files_and_print_results(
    identifier: str,
    backend_model_file_path: Path,
    ts_interface_file_paths: list[Path],
    check_blank: bool = False,
    model_name_conversions: dict[str, list[str]] = {},
) -> bool:
    """
    Check the provided files for the given model and print the results.

    Parameters
    ----------
    identifier : str
        The model in the .ts-backend-check.yaml configuration file to check models and interfaces for.

    backend_model_file_path : Path
        The path to the backend models as defined in the .ts-backend-check.yaml configuration file.

    ts_interface_file_paths : list[Path]
        The paths to the TypeScript interfaces as defined in the .ts-backend-check.yaml configuration file.

    check_blank : bool, default=False
        Whether to also check that fields marked 'blank=True' within Django models are optional (?) in the TypeScript interfaces.

    model_name_conversions : dict[str, list[str]], default={}
        A dictionary of backend model names to their corresponding TypeScript interfaces when snake to camel case isn't valid.

    Returns
    -------
    bool
        Whether the checks passed (True) or not (False).
    """
    if not backend_model_file_path.is_file():
        rprint(
            f"[red]❌ The 'backend_model_file_path' argument, {backend_model_file_path}, is not a valid file. This should be a file that contains the '{identifier}' backend models. Please check the .ts-backend-check.yaml configuration file and try again.[/red]"
        )
        return False

    ts_interface_file_path_validities = [p.is_file() for p in ts_interface_file_paths]
    if invalid_ts_interface_file_paths := [
        str(p)
        for i, p in enumerate(ts_interface_file_paths)
        if not ts_interface_file_path_validities[i]
    ]:
        rprint(
            f"[red]❌ The 'ts_interface_file_paths' argument should contain paths to the '{identifier}' TypeScript types. The following paths do not lead to valid files:\n\n- {'\n- '.join(invalid_ts_interface_file_paths)}\n"
            "\nPlease check the .ts-backend-check.yaml configuration file and try again.[/red]"
        )
        return False

    # We concatenate all contents of the interface files into a single interface.
    # Note: This means that we can't report which interface file the errors are coming from.
    concatenated_types_file = ""
    for p in ts_interface_file_paths:
        with open(p, "r", encoding="utf-8") as f:
            concatenated_types_file += f.read()

    checker = TypeChecker(
        models_file=str(backend_model_file_path),
        concatenated_types_file=concatenated_types_file,
        model_name_conversions=model_name_conversions,
        check_blank=check_blank,
    )

    if missing := checker.check():
        rprint(
            f"\n[red]❌ ts-backend-check error: There are inconsistencies between the provided '{identifier}' backend models and TypeScript interfaces. Please see the output below for details.[/red]"
        )

        for msg in missing:
            rprint(Text.from_markup(f"[red]{msg}[/red]"))

        error_or_errors = "errors" if len(missing) > 1 else "error"
        rprint(
            f"[red]\nPlease fix the {len(missing)} {error_or_errors} above to continue the sync of the backend models of {backend_model_file_path} and the TypeScript interfaces of {ts_interface_file_paths}.[/red]"
        )

        return False

    else:
        rprint(
            f"[green]✅ Success: All backend models are synced with their corresponding TypeScript interfaces for the provided '{identifier}' files.[/green]"
        )

        return True


def main() -> None:
    """
    The main check function to compare a the methods within a backend model to a corresponding TypeScript file.

    Notes
    -----
    The available command line arguments are:
    - --help (-h): Show this help message and exit.
    - --version (-v): Show the version of the ts-backend-check CLI.
    - --upgrade (-u): Upgrade the ts-backend-check CLI to the latest version.
    - --generate-config-file (-gcf): Interactively generate a configuration file for ts-backend-check.
    - --generate-test-project (-gtp): Generate project to test ts-backend-check functionalities.
    - --identifier (-i): The model interface identifier in the .ts-backend-check.yaml configuration file to check.
    - --all (-a): Run checks of all backend models against their corresponding TypeScript interfaces.

    Examples
    --------
    >>> ts-backend-check --generate-config-file  # -gcf
    >>> ts-backend-check --identifier <model-interface-identifier-from-config-file>  # -i
    >>> ts-backend-check --all  # -a
    """
    # MARK: CLI Base

    parser = ArgumentParser(
        prog="ts-backend-check",
        description="Checks the types in TypeScript files against the corresponding backend models.",
        epilog="Visit the codebase at https://github.com/activist-org/ts-backend-check to learn more!",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=60),
    )

    parser._actions[0].help = "Show this help message and exit."

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{get_version_message()}",
        help="Show the version of the ts-backend-check CLI.",
    )

    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        help="Upgrade the ts-backend-check CLI to the latest version.",
    )

    parser.add_argument(
        "-gcf",
        "--generate-config-file",
        action="store_true",
        help="Interactively generate a configuration file for ts-backend-check.",
    )

    parser.add_argument(
        "-gtp",
        "--generate-test-project",
        action="store_true",
        help="Generate project to test ts-backend-check functionalities.",
    )

    parser.add_argument(
        "-i",
        "--identifier",
        help="The model-interface identifier in the .ts-backend-check.yaml configuration file to check.",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Run checks of all backend models against their corresponding TypeScript interfaces.",
    )

    # MARK: Setup CLI

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args == ["--help"]:
        parser.print_help()

    YAML_CONFIG_FILE_PATH = get_config_file_path()

    # MARK: CLI Vars

    if not Path(YAML_CONFIG_FILE_PATH).is_file() and args.generate_config_file:
        generate_config_file()
        return

    if not Path(YAML_CONFIG_FILE_PATH).is_file():
        print(
            "No configuration file. Please generate a configuration file (.ts-backend-check.yaml or .ts-backend-check.yml) with ts-backend-check -gcf."
        )
        exit(1)

    with open(YAML_CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if args.upgrade:
        upgrade_cli()
        return

    if args.generate_config_file:
        generate_config_file()
        return

    if args.generate_test_project:
        generate_test_project()
        return

    # MARK: Run Checks

    results: list[bool] = []

    if args.identifier:
        identifier_config = config.get(args.identifier)

        if not identifier_config:
            rprint(
                f"[red]{args.identifier} is not an index within the .ts-backend-check.yaml configuration file. Please check the defined models and try again.[/red]"
            )
            sys.exit(1)

        config_backend_model_file_path = Path(identifier_config["backend_model_path"])
        config_ts_interface_file_paths = [
            Path(p) for p in identifier_config["ts_interface_paths"]
        ]
        config_check_blank = (
            identifier_config["check_blank_model_fields"]
            if "check_blank_model_fields" in identifier_config
            else False
        )
        config_model_name_conversions = (
            identifier_config["backend_to_ts_model_name_conversions"]
            if "backend_to_ts_model_name_conversions" in identifier_config
            else {}
        )

        r = check_files_and_print_results(
            identifier=args.identifier,
            backend_model_file_path=config_backend_model_file_path,
            ts_interface_file_paths=config_ts_interface_file_paths,
            check_blank=config_check_blank,
            model_name_conversions=config_model_name_conversions,
        )
        results.append(r)

    if args.all:
        for i in config.keys():
            identifier_config = config.get(i)

            config_backend_model_file_path = Path(
                identifier_config["backend_model_path"]
            )
            config_ts_interface_file_paths = [
                Path(p) for p in identifier_config["ts_interface_paths"]
            ]
            config_check_blank = (
                identifier_config["check_blank_model_fields"]
                if "check_blank_model_fields" in identifier_config
                else False
            )
            config_model_name_conversions = (
                identifier_config["backend_to_ts_model_name_conversions"]
                if "backend_to_ts_model_name_conversions" in identifier_config
                else {}
            )

            r = check_files_and_print_results(
                identifier=i,
                backend_model_file_path=config_backend_model_file_path,
                ts_interface_file_paths=config_ts_interface_file_paths,
                check_blank=config_check_blank,
                model_name_conversions=config_model_name_conversions,
            )
            results.append(r)

    if args.identifier or args.all:
        if not all(results):
            sys.exit(1)

        else:
            return  # exit 0

    else:
        rprint(
            "[red]CLI options not recognized. Please see the help directions below.[/red]"
        )
        parser.print_help()


if __name__ == "__main__":
    main()
