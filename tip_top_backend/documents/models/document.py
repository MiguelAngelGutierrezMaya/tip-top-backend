"""Document model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class Document(AuditModel):
    """Document model.

    """

    name = models.CharField(max_length=80, null=False, blank=False)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """Return name."""
        return self.name

    def get_short_name(self):
        """Return name."""
        return self.name
