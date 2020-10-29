"""Level model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class Level(AuditModel):
    """Level model.

    """

    name = models.CharField(max_length=80, null=False, blank=False)
    is_last = models.BooleanField('is_last', default=False)

    # ManyToOne Relations
    parent = models.ForeignKey('levels.Level', blank=True, null=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['name', 'is_last']

    def __str__(self):
        """Return name."""
        return self.name

    def get_short_name(self):
        """Return name."""
        return self.name
