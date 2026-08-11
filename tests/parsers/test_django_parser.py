# SPDX-License-Identifier: GPL-3.0-or-later

import ast

import pytest

from ts_backend_check.parsers.backend_parser import ModelData
from ts_backend_check.parsers.django_parser import DjangoModelParser


def test_extract_model_fields(return_invalid_django_models):
    parser = DjangoModelParser()

    fields = parser.parse(return_invalid_django_models)

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
    parser = DjangoModelParser()
    invalid_model = tmp_path / "invalid_model.py"
    invalid_model.write_text("this is not valid python syntax")

    with pytest.raises(SyntaxError):
        parser.parse(invalid_model)


def test_extract_model_fields_with_empty_file(tmp_path):
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")

    parser = DjangoModelParser()

    fields = parser.parse(empty_file)
    assert fields == ModelData()


def backend_models_to_ignore_from_config(return_invalid_django_models):
    parser = DjangoModelParser()
    fields = parser.parse(return_invalid_django_models)
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
def test_validate_ast_instances(
    django_load_ast, class_name, expected_fields, expected_blank_fields
):
    tree, _ = django_load_ast
    parser = DjangoModelParser()
    node = _get_class_node(tree, class_name)
    fields: list = []
    blank_fields: list = []
    for stmt in node.body:
        if isinstance(stmt, ast.Assign):
            parser._visit_targets(stmt, fields, blank_fields)
    assert fields == fields
    assert blank_fields == blank_fields
