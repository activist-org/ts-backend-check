# SPDX-License-Identifier: GPL-3.0-or-later
"""
Utility functions for ts-backend-check.
"""

from pathlib import Path
from typing import Any

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


def snake_to_camel(input_str: str) -> str:
    """
    Convert snake_case to camelCase while preserving existing camelCase components.

    Parameters
    ----------
    input_str : str
        The snake_case string to convert.

    Returns
    -------
    str
        The camelCase version of the input string.

    Examples
    --------
    hello_world -> helloWorld
    alreadyCamelCase -> alreadyCamelCase
    """
    if not input_str or input_str.startswith("_"):
        return input_str

    words = input_str.split("_")
    result = words[0].lower()

    for word in words[1:]:
        if word:
            if any(c.isupper() for c in word[1:]):
                result += word[0].upper() + word[1:]

            else:
                result += word[0].upper() + word[1:].lower()

    return result


def is_ordered_subset(reference_list: list[Any], candidate_sub_list: list[Any]) -> bool:
    """
    Return True if candidate elements appear in the same relative order as they do in the reference.

    Parameters
    ----------
    reference_list : list
        The original list to reference.

    candidate_sub_list : list
        A potential list that has elements that are in the same relative order to the reference.

    Returns
    -------
    bool
        Whether the candidate elements appear in the same relative order as they do in the reference.
    """
    it = iter(reference_list)
    return all(item in it for item in candidate_sub_list)
