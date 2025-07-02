# SPDX-License-Identifier: AGPL-3.0-or-later
__version__ = "1.0.0"

from .checker import TypeChecker
from .cli.main import main

__all__ = ["main", "TypeChecker"]
