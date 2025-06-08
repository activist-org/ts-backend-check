# SPDX-License-Identifier: GPL-3.0-or-later
"""
Utility functions for ts-backend-check.
"""


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
    hello_world -> helloWorld, alreadyCamelCase -> alreadyCamelCase
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
