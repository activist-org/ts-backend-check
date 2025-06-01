# SPDX-License-Identifier: GPL-3.0-or-later
"""
Utility functions for ts-backend-check.
"""


def snake_to_camel(input_str: str) -> str:
    """
    Convert snake_case to camelCase.

    Parameters
    ----------
    input_str : str
        The snake_case string to convert.

    Returns
    -------
    str
        The camelCase version of the input string.
    """
    components = input_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
