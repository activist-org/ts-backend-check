# SPDX-License-Identifier: GPL-3.0-or-later
"""
Utility functions for ts-backend-check.
"""

from typing import Any


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
