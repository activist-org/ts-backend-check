# SPDX-License-Identifier: GPL-3.0-or-later

from ts_backend_check.parsers.typescript_parser import TypeScriptParser


def test_parse_interfaces(return_invalid_ts_interfaces):
    parser = TypeScriptParser(return_invalid_ts_interfaces)
    interfaces = parser.parse_interfaces()

    # Check Event interface.
    assert "Event" in interfaces

    event = interfaces["Event"]
    assert event.name == "Event"
    assert "title" in event.properties
    assert "organizer" in event.properties
    assert "participants" in event.properties

    assert "Note" not in event.properties  # don't pick up other comments
    assert "Attn" not in event.properties  # don't pick up other comments

    assert "EventExtended" in interfaces

    event_extended = interfaces["EventExtended"]
    assert "date" in event_extended.properties
    assert "isPrivate" in event_extended.properties

    assert "Attn" not in event_extended.properties  # don't pick up other comments

    # Check User interface.
    assert "User" in interfaces
    user = interfaces["User"]
    assert user.name == "User"
    assert "id" in user.properties
    assert "name" in user.properties


def test_get_ignored_fields(return_invalid_ts_interfaces):
    parser = TypeScriptParser(return_invalid_ts_interfaces)
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

    parser = TypeScriptParser(str(tmp_file))
    interfaces = parser.parse_interfaces()

    assert "ExtendedEvent" in interfaces
    extended = interfaces["ExtendedEvent"]
    assert extended.parents == ["BaseEvent"]
    assert "description" in extended.properties
