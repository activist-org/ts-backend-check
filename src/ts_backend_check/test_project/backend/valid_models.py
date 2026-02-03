# SPDX-License-Identifier: GPL-3.0-or-later
"""
Example backend model file that has a valid TS interface file in test_project/frontend.
"""

from django.db import models

# mypy: ignore-errors


class EventModel(models.Model):
    """
    Model for events that has a valid corresponding TS interface file.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey("User", on_delete=models.CASCADE)
    participants = models.ManyToManyField("User", related_name="events")
    is_private = models.BooleanField(default=True)
    date = models.DateTimeField()
    _private_field = models.CharField(max_length=100)  # should be ignored
