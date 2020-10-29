"""UserNotification model."""

# Django
from django.db import models

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class UserNotification(AuditModel):
    """UserNotification model.

    """

    date = models.DateField(null=False)

    # ManyToOne Relations
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    notification = models.ForeignKey('notifications.Notification', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['date']

    def __str__(self):
        """Return empty."""
        return ""

    def get_short_name(self):
        """Return empty."""
        return ""
