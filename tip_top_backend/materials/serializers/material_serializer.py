"""Material serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.lessons.serializers.lesson_serializer import LessonModelSerializer

# Model
from tip_top_backend.materials.models import Material


class MaterialModelSerializer(serializers.ModelSerializer):
    """Material model serializer"""

    lesson = LessonModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Material
        fields = (
            'id',
            'name',
            'type',
            'url',
            'lesson'
        )


class MaterialSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """Material sign up serializer.

    Handle sign up data validation and material creation.
    """

    lesson_id = serializers.IntegerField(write_only=True)
    type = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=150)
    url = serializers.URLField(max_length=200)

    def create(self, data):
        """Handle material creation."""
        student = Material.objects.create(**data)
        return student
