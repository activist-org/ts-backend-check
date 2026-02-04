# SPDX-License-Identifier: GPL-3.0-or-later
"""
Example backend model file that has both valid and invalid TS interface files in test_project/frontend.
"""

from django.db import models

# mypy: ignore-errors


class EventModel(models.Model):
    """
    Model for events that has both valid and invalid corresponding TS interface files.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey("User", on_delete=models.CASCADE)
    participants = models.ManyToManyField("User", related_name="events", blank=True)
    is_private = models.BooleanField(default=True)
    date = models.DateTimeField()
    _private_field = models.CharField(max_length=100)  # should be ignored
