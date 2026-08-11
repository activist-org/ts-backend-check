# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for BackendModelParser (abstract base class).

Strategy
--------
BackendModelParser can't be instantiated directly because it's an abstract base class.
It has three abstract methods: MODEL_TEXT_REGEX, ALL_MODEL_FIELDS_ORDERED_REGEX, and _build_models.
To test it's shared logic (_load_ast, _should_ignore,_extract_inherited_fields and the two class level inherit regexes),
we create a minimal subclass that implements the abstract methods and properties in isolation from Django/FastAPI-specific parsing.
We define a minimal concrete subclass of BackendModelParser that implements just enough to be instantiated.

This keeps the tests independent of DjangoModelParser / FastAPIModelParser.
"""

import ast

import pytest

from tests.parsers.helpers import MinimalParser
from ts_backend_check.parsers.backend_parser import BackendModelParser


# MARK: Load ast
def test_load_ast_parses_valid_file(tmp_path, parser):
    file = tmp_path / "valid.py"
    file.write_text("class Foo:\n    bar: int\n")

    tree, content = parser._load_ast(file)
    assert isinstance(tree, ast.Module)
    assert "class Foo" in content


def test_load_ast_strips_leading_blank_lines(tmp_path, parser):
    file = tmp_path / "leading_blank.py"
    file.write_text("\n\n\nclass Foo:\n    bar: int\n")

    _, content = parser._load_ast(file)

    assert content.startswith("class Foo")


@pytest.mark.parametrize(
    "file_name,file_content,create_file,expected_exception",
    [
        ("bad.py", "class Foo(:\n   bar int\n)", True, SyntaxError),
        ("does_not_exist.py", None, False, FileNotFoundError),
    ],
)
def test_load_ast_raises_on_bad_input(
    tmp_path, parser, file_name, file_content, create_file, expected_exception
):
    file = tmp_path / file_name
    if create_file:
        file.write_text(file_content)
    with pytest.raises(expected_exception):
        parser._load_ast(file)


# MARK: Should Ignore


@pytest.mark.parametrize(
    "models_to_ignore,class_name,expected",
    [
        (["Foo", "Bar"], "Foo", True),
        (["Foo", "Bar"], "Baz", False),
        (None, "Foo", False),
        ([], "Baz", False),
    ],
)
def test_should_ignore(models_to_ignore, class_name, expected):
    parser = MinimalParser(models_to_ignore)
    assert parser._should_ignore(class_name) is expected


# MARK: Inherit Regexes
@pytest.mark.parametrize(
    "comment,expected",
    [
        ("# tsbc: inherit BaseModel", "BaseModel"),
        ("# ts-backend-check: inherit OtherModel", "OtherModel"),
    ],
)
def test_inherit_field_comment_regex_matches(comment, expected):
    match = BackendModelParser.INHERIT_FIELD_COMMENT_REGEX.search(comment)
    assert match is not None
    assert match.group(1) == expected


def test_inherit_field_comment_regex_excludes_blank_true():
    comment = "# tsbc: inherit BaseModel (blank=True)"
    match = BackendModelParser.INHERIT_FIELD_COMMENT_REGEX.search(comment)
    assert match is None


def test_inherit_field_comment_regex_no_match_on_unrelated_comment():
    comment = "# just a regular comment"
    match = BackendModelParser.INHERIT_FIELD_COMMENT_REGEX.search(comment)
    assert match is None


def test_inherit_blank_field_comment_regex_matches():
    comment = "# tsbc: inherit BaseModel (blank=True)"
    match = BackendModelParser.INHERIT_BLANK_FIELD_COMMENT_REGEX.search(comment)
    assert match is not None
    assert match.group(1) == "BaseModel"


def test_inherit_blank_field_comment_regex_no_match_without_blank_true():
    comment = "# tsbc: inherit BaseModel"
    match = BackendModelParser.INHERIT_BLANK_FIELD_COMMENT_REGEX.search(comment)
    assert match is None


# MARK: Extract Inherited Fields.


def test_extract_inherited_fields_no_models_returns_empty_dict(parser):
    assert parser._extract_inherited_fields("no models here at all ") == {}


def test_extract_inherited_fields_direct_inherit(parser):
    content = "BODY:# tsbc: inherit BaseModel\nsome text:NAME:Foo:END"
    result = parser._extract_inherited_fields(content)
    assert result == {
        "Foo": {"inherited_fields": ["BaseModel"], "inherited_blank_fields": []}
    }


def test_extract_inherited_fields_multiple_models(parser):
    content = (
        "BODY:# tsbc: inherit BaseModel\n:NAME:Foo:END"
        "BODY:# tsbc: inherit OtherModel (blank=True)\n:NAME:Bar:END"
    )

    result = parser._extract_inherited_fields(content)

    assert set(result.keys()) == {"Foo", "Bar"}
    assert result["Foo"]["inherited_fields"] == ["BaseModel"]
    assert result["Bar"]["inherited_blank_fields"] == ["OtherModel"]
