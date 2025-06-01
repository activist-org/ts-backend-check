# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the ts-backend-check command line interface.
"""

import sys

import click

from ..checker import TypeChecker


@click.group()
@click.version_option()
def cli():
    """
    TS Backend Check is a Python package used to check TypeScript types against their corresponding backend models.
    """
    pass


@cli.command()
@click.argument("backend_model", type=click.Path(exists=True))
@click.argument("typescript_file", type=click.Path(exists=True))
def check(backend_model: str, typescript_file: str):
    """
    Check TypeScript types against backend models.

    This command checks if all fields from the backend model are properly represented
    in the TypeScript types file. It supports marking fields as backend-only using
    special comments in the TypeScript file.

    Parameters
    ----------
    backend_model : str
        The path to the backend model file (e.g. Python class).

    typescript_file : str
        The path to the TypeScript interface/type file.

    Examples
    --------
    ts-backend-check check src/models/user.py src/types/user.ts
    """
    checker = TypeChecker(models_file=backend_model, types_file=typescript_file)
    if missing := checker.check():
        click.echo("Missing TypeScript fields found:")
        click.echo("\n".join(missing))
        click.echo(
            f"\nPlease correct the {len(missing)} fields above to have backend models and frontend types fully synced."
        )
        sys.exit(1)

    click.echo("All model fields are properly typed in TypeScript!")


if __name__ == "__main__":
    cli()
