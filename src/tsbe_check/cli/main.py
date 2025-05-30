# SPDX-License-Identifier: GPL-3.0-or-later
"""
Setup and commands for the tsbe-check command line interface.
"""

import click


@click.group()
@click.version_option()
def cli():
    """tsbe-check is a Python package used to check TypeScript types against their corresponding backend models."""
    pass


@cli.command()
@click.argument("typescript_file", type=click.Path(exists=True))
@click.argument("backend_model", type=click.Path(exists=True))
def check(typescript_file: str, backend_model: str):
    click.echo(f"Checking {typescript_file} against {backend_model}")


if __name__ == "__main__":
    cli()
