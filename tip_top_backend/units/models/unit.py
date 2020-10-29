"""Unit model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class Unit(AuditModel):
    """Unit model.

    """

    name = models.CharField(max_length=80, null=False, blank=False)
    is_last = models.BooleanField('is_last', default=False)

    # ManyToOne Relations
    level = models.ForeignKey('levels.Level', on_delete=models.CASCADE)
    parent = models.ForeignKey('units.Unit', blank=True, null=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['name', 'is_last']

    def __str__(self):
        """Return name."""
        return self.name

    def get_short_name(self):
        """Return name."""
        return self.name
