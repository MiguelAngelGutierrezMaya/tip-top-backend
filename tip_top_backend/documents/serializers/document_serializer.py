"""Document serializer."""

# Django REST framework
from rest_framework import serializers

# Model
from tip_top_backend.documents.models import Document


class DocumentModelSerializer(serializers.ModelSerializer):
    """Document model serializer."""

    class Meta:
        """Meta class."""
        model = Document
        fields = [
            'id',
            'name',
        ]
