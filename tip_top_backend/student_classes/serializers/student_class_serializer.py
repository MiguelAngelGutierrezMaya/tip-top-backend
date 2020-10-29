"""StudentClass serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.students.serializers.student_serializer import StudentModelSerializer
from tip_top_backend.classes.serializers.class_serializer import ClassModelSerializer

# Model
from tip_top_backend.student_classes.models import StudentClass


class StudentClassModelSerializer(serializers.ModelSerializer):
    """StudentClass model serializer"""

    student = StudentModelSerializer(read_only=True)
    class_obj = ClassModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = StudentClass
        fields = (
            'id',
            'student',
            'class_obj'
        )


class StudentClassSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """StudentClass sign up serializer.

    Handle sign up data validation and studentClass creation.
    """

    student_id = serializers.IntegerField(write_only=True)
    class_obj_id = serializers.IntegerField(write_only=True)

    def create(self, data):
        """Handle student creation."""
        student_class = StudentClass.objects.create(**data)
        return student_class
