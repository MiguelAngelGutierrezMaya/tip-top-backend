"""Student model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel
from tip_top_backend.utils.constants import Constants


class Student(AuditModel):
    """Student model.

    """

    genre = models.CharField(
        max_length=30,
        choices=Constants.GENRES,
        default=Constants.MALE,
    )
    teacher = models.IntegerField(blank=True, null=True, default=0)

    # ManyToOne Relations
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    current_lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)

    def __str__(self):
        """Return username."""
        return ""

    def get_short_name(self):
        """Return username."""
        return ""
