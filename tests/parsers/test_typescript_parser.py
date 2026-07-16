# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from ts_backend_check.parsers.typescript_parser import TypeScriptParser


@pytest.fixture
def parser_fixture_file(request):
    fixture_name = {
        "django": "return_invalid_django_concatenated_types_file",
        "fastapi": "return_invalid_fastapi_concatenated_types_file",
    }[request.param]
    return request.getfixturevalue(fixture_name)


@pytest.mark.parametrize(
    "parser_fixture_file, interface_name, expected_properties, excluded_properties",
    [
        pytest.param(
            "django",
            "Event",
            ["title", "organizer", "participants"],
            ["Note", "Attn"],
            id="django-event",
        ),
        pytest.param(
            "django",
            "EventExtended",
            ["date", "isPrivate"],
            ["Attn"],
            id="django-event_extended",
        ),
        pytest.param("django", "User", ["id", "name"], [], id="django-user"),
        pytest.param(
            "fastapi",
            "Event",
            ["title", "organizer", "participants"],
            ["Note", "Attn"],
            id="fastapi-event",
        ),
        pytest.param(
            "fastapi",
            "EventExtended",
            ["date", "isPrivate"],
            ["Attn"],
            id="fastapi-event_extended",
        ),
        pytest.param("fastapi", "User", ["id", "name"], [], id="fastapi-user"),
    ],
    indirect=["parser_fixture_file"],
)
def test_parse_interfaces(
    parser_fixture_file, interface_name, expected_properties, excluded_properties
):
    parser = TypeScriptParser(parser_fixture_file)
    interfaces = parser.parse_interfaces()

    assert interface_name in interfaces
    interface = interfaces[interface_name]
    assert interface.name == interface_name
    for prop in expected_properties:
        assert prop in interface.properties
    for prop in excluded_properties:
        assert prop not in interface.properties


@pytest.mark.parametrize(
    "parser_fixture_file", ["django", "fastapi"], indirect=["parser_fixture_file"]
)
def test_get_ignored_fields(parser_fixture_file):
    parser = TypeScriptParser(parser_fixture_file)
    backend_only = parser.get_ignored_fields()

    assert "date" in backend_only  # date is ignored


def test_parse_interfaces_with_extends(tmp_path):
    ts_content = """
    interface BaseEvent {
        id: number;
        title: string;
    }

    export interface ExtendedEvent extends BaseEvent {
        description: string;
    }
    """

    tmp_file = tmp_path / "extended.ts"
    tmp_file.write_text(ts_content)

    with open(tmp_file, "r", encoding="utf-8") as f:
        concatenated_types_file = f.read()

    parser = TypeScriptParser(concatenated_types_file)
    interfaces = parser.parse_interfaces()

    assert "ExtendedEvent" in interfaces

    extended = interfaces["ExtendedEvent"]
    assert extended.parents == ["BaseEvent"]
    assert "description" in extended.properties
