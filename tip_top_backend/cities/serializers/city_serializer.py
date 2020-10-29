"""City serializer."""

# Django REST framework
from rest_framework import serializers

# Serializers
from tip_top_backend.states.serializers.state_serializer import StateModelSerializer

# Model
from tip_top_backend.cities.models import City


class CityModelSerializer(serializers.ModelSerializer):
    """City model serializer."""

    state = StateModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = City
        fields = [
            'id',
            'name',
            'state'
        ]
