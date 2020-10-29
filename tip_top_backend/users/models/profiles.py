"""Profile model."""

# Django
from django.db import models

# Utilities
from tip_top_backend.utils.audit_model import AuditModel


class Profile(AuditModel):
    """Profile model.

    A profile holds a user's public data like, picture,
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    url = models.URLField(max_length=200)

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
