# SPDX-License-Identifier: GPL-3.0-or-later
"""
Tests for  ParserContext.
"""

import pytest

from ts_backend_check.parsers.context_parser import ParserContext
from ts_backend_check.parsers.django_parser import DjangoModelParser
from ts_backend_check.parsers.fastapi_parser import FastAPIModelParser


class TestParserContextSelection:
    def test_selects_django_parser(self):
        context = ParserContext(backend_type="django")
        assert isinstance(context._parser, DjangoModelParser)

    def test_selects_fastapi_parser(self):
        context = ParserContext(backend_type="fastapi")
        assert isinstance(context._parser, FastAPIModelParser)

    def test_invalid_backend_type_raises(self):
        with pytest.raises(
            ValueError, match="Unsupported backend type: invalid_backend"
        ):
            ParserContext(backend_type="invalid_backend")
