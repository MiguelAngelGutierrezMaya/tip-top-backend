"""Country serializer."""

# Django REST framework
from rest_framework import serializers

# Model
from tip_top_backend.countries.models import Country


class CountryModelSerializer(serializers.ModelSerializer):
    """State model serializer."""

    class Meta:
        """Meta class."""
        model = Country
        fields = [
            'name'
        ]
