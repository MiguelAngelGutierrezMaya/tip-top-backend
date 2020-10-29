"""Role model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel
from tip_top_backend.utils.constants import Constants


class Role(AuditModel):
    """Role model.

    """

    name = models.CharField(
        max_length=30,
        choices=Constants.ROLE_OPTIONS,
        default=Constants.ROLE_USER,
    )

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """Return name."""
        return self.name

    def get_short_name(self):
        """Return name."""
        return self.name
