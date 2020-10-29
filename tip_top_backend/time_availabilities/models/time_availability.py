"""TimeAvailability model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel
from tip_top_backend.utils.constants import Constants


class TimeAvailability(AuditModel):
    """TimeAvailability model.

    """

    init = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    type = models.CharField(max_length=30, choices=Constants.TYPE_NOTIFICATIONS)

    # ManyToOne Relations
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['init', 'end', 'type']

    def __str__(self):
        """Return empty."""
        return ""

    def get_short_name(self):
        """Return empty."""
        return ""
