"""Comment model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class Comment(AuditModel):
    """Comment model.

    """

    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False)
    date = models.DateTimeField(null=False)

    # ManyToOne Relations
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['title', 'content', 'date']

    def __str__(self):
        """Return title."""
        return self.title

    def get_short_name(self):
        """Return title."""
        return self.title
