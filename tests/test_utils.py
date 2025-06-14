# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for utility functions in ts-backend-check.
"""

from ts_backend_check.utils import snake_to_camel


def test_snake_to_camel():
    assert snake_to_camel("hello_world") == "helloWorld"
    assert snake_to_camel("test_case") == "testCase"
    assert snake_to_camel("already_camelCase") == "alreadyCamelCase"
    assert snake_to_camel("multiple_word_test") == "multipleWordTest"
    assert snake_to_camel("single") == "single"


def test_snake_to_camel_edge_cases():
    assert snake_to_camel("") == ""
    assert snake_to_camel("_") == "_"
    assert snake_to_camel("__") == "__"
    assert snake_to_camel("_private") == "_private"
