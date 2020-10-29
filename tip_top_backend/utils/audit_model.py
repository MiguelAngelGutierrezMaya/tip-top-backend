"""Django model utilities."""

# Django
from django.db import models


class AuditModel(models.Model):
    """Audit Base Model.

    AuditModel acts an abstract base class from wich every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime object was created.
        + modified (DateTime): Store the last datetime object was modified.
    """
    created = models.DateTimeField(
        'Created At',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        'Created At',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        """Meta options."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']
