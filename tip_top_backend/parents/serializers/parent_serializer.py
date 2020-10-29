"""Parent serializer."""

# Django REST framework
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from rest_framework import serializers

# Serializers
from tip_top_backend.students.serializers.student_serializer import StudentModelSerializer

# Model
from tip_top_backend.parents.models import Parent


class ParentModelSerializer(serializers.ModelSerializer):
    """Parent model serializer"""

    student = StudentModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Parent
        fields = (
            'first_name',
            'last_name',
            'type_parent',
            'student',
        )


class ParentSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """Parent sign up serializer.

    Handle sign up data validation and parent creation.
    """

    student_id = serializers.IntegerField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    type_parent = serializers.CharField(max_length=50)

    def create(self, data):
        """Handle student creation."""
        student = Parent.objects.create(**data)
        return student
