# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import ast
import textwrap

from ts_backend_check.parsers.django_parser import extract_model_fields, DjangoModelVisitor


def test_extract_model_fields(return_invalid_django_models):
    fields = extract_model_fields(return_invalid_django_models)

    assert "EventModel" in fields[0]
    event_fields = fields[0]["EventModel"]

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
    invalid_model = tmp_path / "invalid_model.py"
    invalid_model.write_text("this is not valid python syntax")

    with pytest.raises(SyntaxError):
        extract_model_fields(str(invalid_model))


def test_extract_model_fields_with_empty_file(tmp_path):
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")

    fields = extract_model_fields(str(empty_file))
    assert fields == ({}, {})

def make_visitor(source: str) -> DjangoModelVisitor:
    """Parse *source* and return a visited DjangoModelVisitor."""
    source = textwrap.dedent(source).strip()
    tree = ast.parse(source)
    visitor = DjangoModelVisitor(source.splitlines())
    visitor.visit(tree)
    return visitor

def test_tagged_class_is_excluded_from_models():
    source = """
    class AuditLog(models.Model):  #tsbc: backend_only_model
        action = models.CharField(max_length=100)
        timestamp = models.DateTimeField()
    """
    v = make_visitor(source)
    print(v.models)
    assert "AuditLog" not in v.models
