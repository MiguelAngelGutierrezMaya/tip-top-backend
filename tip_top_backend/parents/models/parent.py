"""Parent model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class Parent(AuditModel):
    """Parent model.

    """

    first_name = models.CharField('Nombres', max_length=50, null=False, blank=False)
    last_name = models.CharField('Apellidos', max_length=80, null=False, blank=False)
    type_parent = models.CharField('Parentezco', max_length=50, null=False, blank=False)

    # ManyToOne Relations
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)

    def __str__(self):
        """Return first_name."""
        return self.first_name

    def get_short_name(self):
        """Return first_name."""
        return self.first_name
