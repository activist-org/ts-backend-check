# SPDX-License-Identifier: GPL-3.0-or-later

from ts_backend_check.parsers.typescript_parser import TypeScriptParser


def test_parse_interfaces(temp_typescript_file):
    parser = TypeScriptParser(temp_typescript_file)
    interfaces = parser.parse_interfaces()

    # Check Event interface.
    assert "Event" in interfaces
    event = interfaces["Event"]
    assert event.name == "Event"
    assert "title" in event.fields
    assert "description" in event.fields
    assert "isActive" in event.fields
    assert "organizer" in event.fields

    # Check User interface.
    assert "User" in interfaces
    user = interfaces["User"]
    assert user.name == "User"
    assert "id" in user.fields
    assert "name" in user.fields


def test_get_ignored_fields(temp_typescript_file):
    parser = TypeScriptParser(temp_typescript_file)
    backend_only = parser.get_ignored_fields()

    assert "date" in backend_only
    assert "participants" in backend_only


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

    parser = TypeScriptParser(str(tmp_file))
    interfaces = parser.parse_interfaces()

    assert "ExtendedEvent" in interfaces
    extended = interfaces["ExtendedEvent"]
    assert extended.parents == ["BaseEvent"]
    assert "description" in extended.fields
