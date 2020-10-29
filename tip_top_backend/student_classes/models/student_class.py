"""StudentClass model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class StudentClass(AuditModel):
    """StudentClass model.

    """

    # ManyToOne Relations
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    class_obj = models.ForeignKey('classes.Class', on_delete=models.CASCADE)

    def __str__(self):
        """Return empty."""
        return ""

    def get_short_name(self):
        """Return empty."""
        return ""
