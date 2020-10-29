"""Notification serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Model
from tip_top_backend.notifications.models import Notification


class NotificationModelSerializer(serializers.ModelSerializer):
    """Notification model serializer."""

    class Meta:
        """Meta class."""
        model = Notification
        fields = [
            'id',
            'title',
            'type',
            'status',
            'data',
            'to',
            'template'
        ]


class NotificationSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """Notification sign up serializer.

    Handle sign up data validation and Notification creation.
    """
    
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=150)
    type = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=30)
    data = serializers.JSONField()
    to = serializers.EmailField()
    template = serializers.CharField(max_length=120)

    def create(self, data):
        """Handle Notification creation."""
        notification = Notification.objects.create(**data)
        return notification
