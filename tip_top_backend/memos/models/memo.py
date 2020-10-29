"""Memo model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel
from tip_top_backend.utils.constants import Constants


class Memo(AuditModel):
    """Memo model.

    """

    date = models.DateTimeField(null=False)
    vocabulary_learned = models.TextField(null=False)
    sentences_learned = models.TextField(null=False)
    comments = models.TextField(null=False)
    type = models.CharField(
        max_length=30,
        choices=Constants.TYPE_MEMOS,
        default=Constants.DRAFT,
    )

    # ManyToOne Relations
    student_class = models.ForeignKey('student_classes.StudentClass', on_delete=models.CASCADE)

    def __str__(self):
        """Return empty."""
        return ""

    def get_short_name(self):
        """Return empty."""
        return ""
