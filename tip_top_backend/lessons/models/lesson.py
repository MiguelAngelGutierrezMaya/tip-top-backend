"""Lesson model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class Lesson(AuditModel):
    """Lesson model.

    """

    title = models.CharField(max_length=150, null=False, blank=False)
    is_last = models.BooleanField('is_last', default=False)

    # ManyToOne Relations
    unit = models.ForeignKey('units.Unit', on_delete=models.CASCADE)
    parent = models.ForeignKey('lessons.Lesson', blank=True, null=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['title', 'is_last']

    def __str__(self):
        """Return title."""
        return self.title

    def get_short_name(self):
        """Return title."""
        return self.title
