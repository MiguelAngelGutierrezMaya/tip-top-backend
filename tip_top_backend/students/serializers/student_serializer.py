"""Student serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.users.serializers.user_serializer import UserModelSerializer
from tip_top_backend.lessons.serializers.lesson_serializer import LessonModelSerializer

# Model
from tip_top_backend.students.models import Student


class StudentModelSerializer(serializers.ModelSerializer):
    """Student model serializer"""

    user = UserModelSerializer(read_only=True)
    current_lesson = LessonModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Student
        fields = (
            'id',
            'user',
            'teacher',
            'current_lesson'
        )


class StudentSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """Student sign up serializer.

    Handle sign up data validation and student creation.
    """

    user_id = serializers.IntegerField(write_only=True)
    teacher = serializers.IntegerField(write_only=True, default=None)
    current_lesson_id = serializers.IntegerField(write_only=True)
    genre = serializers.CharField(max_length=30)

    def create(self, data):
        """Handle student creation."""
        student = Student.objects.create(**data)
        return student
