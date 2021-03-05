"""ClassRepetition model."""

# Django
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class ClassRepetition(AuditModel):
    """ClassRepetition model.

    """

    last_repeat_date = models.DateTimeField(null=False)
    days = ArrayField(models.BooleanField(default=False), null=False)

    def __str__(self):
        """Return empty."""
        return ""

    def get_short_name(self):
        """Return empty."""
        return ""
