"""Level serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


# Model
from tip_top_backend.levels.models import Level


class ParentLevelModelSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """Parent Level model serializer."""

    class Meta:
        """Meta class."""
        model = Level
        fields = [
            'id',
            'name'
        ]
