# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for utility functions in ts-backend-check.
"""

from ts_backend_check.utils import is_ordered_subset, snake_to_camel


def test_snake_to_camel():
    assert snake_to_camel(input_str="hello_world") == "helloWorld"
    assert snake_to_camel(input_str="test_case") == "testCase"
    assert snake_to_camel(input_str="partially_camelCase") == "partiallyCamelCase"
    assert snake_to_camel(input_str="multiple_word_test") == "multipleWordTest"
    assert snake_to_camel(input_str="single") == "single"


def test_snake_to_camel_edge_cases():
    assert snake_to_camel(input_str="") == ""
    assert snake_to_camel(input_str="_") == "_"
    assert snake_to_camel(input_str="__") == "__"
    assert snake_to_camel(input_str="_private") == "_private"


def test_is_ordered_subset():
    assert is_ordered_subset([1, 2, 3], [1, 2])
    assert is_ordered_subset([1, 2, 3], [2])
    assert not is_ordered_subset([1, 2, 3], [2, 1])
