# SPDX-License-Identifier: GPL-3.0-or-later

import ast

import pytest

from ts_backend_check.parsers.backend_parser import ModelData
from ts_backend_check.parsers.fastapi_parser import FastAPIModelParser


# Regex Test
def test_extract_model_fields(return_invalid_fastapi_models):
    parser = FastAPIModelParser()
    fields = parser.parse(return_invalid_fastapi_models)

    assert "EventModel" in fields.models_all_fields
    event_fields = fields.models_all_fields["EventModel"]

    # Check that all non-private fields are extracted.
    assert "title" in event_fields
    assert "description" in event_fields
    assert "organizer" in event_fields
    assert "participants" in event_fields
    assert "is_private" in event_fields
    assert "date" in event_fields

    # Check that private fields are ignored.
    assert "_private_field" not in event_fields


def test_extract_model_fields_with_invalid_syntax(tmp_path):
    parser = FastAPIModelParser()
    invalid_model = tmp_path / "invalid_model.py"
    invalid_model.write_text("this is not valid python syntax")

    with pytest.raises(SyntaxError):
        parser.parse(invalid_model)


def test_extract_model_fields_with_empty_file(tmp_path):
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")

    parser = FastAPIModelParser()

    fields = parser.parse(empty_file)
    assert fields == ModelData()


def backend_models_to_ignore_from_config(return_invalid_fastapi_models):
    parser = FastAPIModelParser()
    fields = parser.parse(return_invalid_fastapi_models)
    assert fields.models_all_fields[0] == "BackendOnlyModel"


def _get_class_node(tree: ast.AST, class_name: str) -> ast.ClassDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise ValueError(f"Class {class_name!r} not found in AST")


@pytest.mark.parametrize(
    "class_name, expected_fields, expected_blank_fields",
    [
        (
            "EventModel",
            ["title", "description", "organizer", "participants", "is_private", "date"],
            ["participants"],
        )
    ],
)
def test_visit_annassign(
    fastapi_load_ast, class_name, expected_fields, expected_blank_fields
):
    tree, _ = fastapi_load_ast
    parser = FastAPIModelParser()
    node = _get_class_node(tree, class_name)
    fields: list = []
    blank_fields: list = []
    parser._visit_annassign(node, fields, blank_fields)

    assert fields == expected_fields
    assert blank_fields == expected_blank_fields
