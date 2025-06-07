import os
import pytest
from pathlib import Path


@pytest.fixture
def sample_django_model():
    return """
from django.db import models

class EventModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    organizer = models.ForeignKey('User', on_delete=models.CASCADE)
    participants = models.ManyToManyField('User', related_name='events')
    _private_field = models.CharField(max_length=100)  # Should be ignored
"""


@pytest.fixture
def sample_typescript_interface():
    return """
export interface Event {
    title: string;
    description: string;
    // Note: date is backend only
    isActive: boolean;
    organizer: User;
    // participants is backend only
}

export interface User {
    id: number;
    name: string;
}
"""


@pytest.fixture
def temp_django_model(tmp_path, sample_django_model):
    model_file = tmp_path / "models.py"
    model_file.write_text(sample_django_model)
    return str(model_file)


@pytest.fixture
def temp_typescript_file(tmp_path, sample_typescript_interface):
    ts_file = tmp_path / "types.ts"
    ts_file.write_text(sample_typescript_interface)
    return str(ts_file)
