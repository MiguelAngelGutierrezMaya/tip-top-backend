"""Student model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel
from tip_top_backend.utils.constants import Constants


class Material(AuditModel):
    """Material model.

    """

    name = models.CharField(max_length=150, null=True)
    url = models.URLField(max_length=200)
    type = models.CharField(max_length=30, choices=Constants.TYPE_MATERIALS, default=Constants.TYPE_URL)

    # ManyToOne Relations
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['url', 'name', 'type']

    def __str__(self):
        """Return username."""
        return ""

    def get_short_name(self):
        """Return username."""
        return ""
