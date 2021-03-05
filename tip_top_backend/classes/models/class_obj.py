"""Class model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel

# Django Enviroment
import environ
env = environ.Env()


class Class(AuditModel):
    """Class model.

    """

    init = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    state = models.BooleanField('state', default=True)
    url = models.URLField('Enlace de videollamada', max_length=200, default=env('DJANGO_MEDIA_URL'))

    # ManyToOne Relations
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    class_repetition = models.ForeignKey('class_repetitions.ClassRepetition', null=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['init', 'end']

    def __str__(self):
        """Return empty."""
        return ""

    def get_short_name(self):
        """Return empty."""
        return ""
