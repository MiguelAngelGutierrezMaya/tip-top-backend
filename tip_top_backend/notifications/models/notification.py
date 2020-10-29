"""Notification model."""

# Django
from django.contrib.postgres.fields import JSONField
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel
from tip_top_backend.utils.constants import Constants


class Notification(AuditModel):
    """Notification model.

    """

    title = models.CharField(max_length=150, null=True)

    type = models.CharField(max_length=20, choices=Constants.TYPE_NOTIFICATIONS, default=Constants.TYPE_EMAIL)

    status = models.CharField(
        max_length=30,
        choices=Constants.STATUS_NOTIFICATIONS,
        default=Constants.STATUS_PENDING
    )

    data = JSONField()

    to = models.EmailField(max_length=250, null=True)

    template = models.CharField(max_length=120, null=True)

    REQUIRED_FIELDS = ['title', 'type', 'status', 'data', 'to', 'template']

    def __str__(self):
        """Return title."""
        return ""

    def get_short_name(self):
        """Return title."""
        return self.title
