# SPDX-License-Identifier: GPL-3.0-or-later
"""
Example FastAPI backend model file that has both valid and invalid TS interface files in test_project/frontend.
"""

from datetime import datetime

from pydantic import BaseModel  # ty: ignore[unresolved-import]


class EventModel(BaseModel):
    """
    FastAPI model for events that has both valid and invalid corresponding TS interface files.
    """

    title: str
    description: str
    organizer: str
    participants: list[str] | None
    is_private: bool
    date: datetime
    _private_field: str  # should be ignored


class UserModel(BaseModel):
    """
    FastAPI model for users that has both valid and invalid corresponding TS interface files.
    """

    id: str
    name: str
    # tsbc: inherit email (blank=True)
    # ts-backend-check: from AbstractUser inherit password


class BackendOnlyModel(BaseModel):
    """
    FastAPI model that's only for the backend and is ignored via the 'backend_models_to_ignore' configuration option.
    """

    id: str
