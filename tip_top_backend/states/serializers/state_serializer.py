"""State serializer."""

# Django REST framework
from rest_framework import serializers

# Serializers
from tip_top_backend.countries.serializers.country_serializer import CountryModelSerializer

# Model
from tip_top_backend.states.models import State


class StateModelSerializer(serializers.ModelSerializer):
    """State model serializer."""

    country = CountryModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = State
        fields = [
            'name',
            'country'
        ]
