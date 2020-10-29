"""TimeAvailabilitySerializer serializer."""

# Django REST framework
from rest_framework import serializers

# Serializers
from tip_top_backend.users.serializers.user_serializer import UserModelSerializer

# Model
from tip_top_backend.time_availabilities.models import TimeAvailability


class TimeAvailabilityModelSerializer(serializers.ModelSerializer):
    """TimeAvailability model serializer."""

    user = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = TimeAvailability
        fields = [
            'datetime_init',
            'datetime_end',
            'type',
            'user'
        ]
