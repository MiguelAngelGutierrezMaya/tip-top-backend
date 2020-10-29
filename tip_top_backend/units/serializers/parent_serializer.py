"""Unit serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


# Model
from tip_top_backend.units.models import Unit


class ParentUnitModelSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """Parent Unit model serializer."""

    class Meta:
        """Meta class."""
        model = Unit
        fields = [
            'id',
            'name'
        ]
