# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the tsbe-check command line interface.
"""

import sys

import click

from ..checker import TypeChecker


@click.group()
@click.version_option()
def cli():
    """tsbe-check is a Python package used to check TypeScript types against their corresponding backend models."""
    pass


@cli.command()
@click.argument("typescript_file", type=click.Path(exists=True))
@click.argument("backend_model", type=click.Path(exists=True))
def check(typescript_file: str, backend_model: str):
    """Check TypeScript types against backend models.

    This command checks if all fields from the backend model are properly represented
    in the TypeScript types file. It supports marking fields as backend-only using
    special comments in the TypeScript file.

    Example usage:
    tsbe-check check src/types/user.ts src/models/user.py
    """
    checker = TypeChecker(backend_model, typescript_file)
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
