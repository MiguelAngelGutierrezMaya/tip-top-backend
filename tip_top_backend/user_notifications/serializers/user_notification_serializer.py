"""UserNotification serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.users.serializers.user_serializer import UserModelSerializer
from tip_top_backend.notifications.serializers.notification_serializer import NotificationModelSerializer

# Model
from tip_top_backend.user_notifications.models import UserNotification


class UserNotificationModelSerializer(serializers.ModelSerializer):
    """UserNotification model serializer."""

    user = UserModelSerializer(read_only=True)
    notification = NotificationModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = UserNotification
        fields = [
            'date',
            'user',
            'notification'
        ]


class UserNotificationSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """UserNotification sign up serializer.

    Handle sign up data validation and UserNotification creation.
    """

    date = serializers.DateTimeField()
    user_id = serializers.IntegerField(write_only=True)
    notification_id = serializers.IntegerField(write_only=True)

    def create(self, data):
        """Handle UserNotification creation."""
        user_notification = UserNotification.objects.create(**data)
        return user_notification
