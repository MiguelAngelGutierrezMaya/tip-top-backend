"""City model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class City(AuditModel):
    """City model.

    """

    name = models.CharField(max_length=80, null=False, blank=False)

    # ManyToOne Relations
    state = models.ForeignKey('states.State', default=1, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """Return name."""
        return self.name

    def get_short_name(self):
        """Return name."""
        return self.name
