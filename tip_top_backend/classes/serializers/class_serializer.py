"""Class serializer."""

# Dependencies
import datetime

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.lessons.serializers.lesson_serializer import LessonModelSerializer
from tip_top_backend.users.serializers.user_serializer import UserModelSerializer

# Model
from tip_top_backend.classes.models import Class


class ClassModelSerializer(serializers.ModelSerializer):
    """Class model serializer."""

    lesson = LessonModelSerializer(read_only=True)
    user = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Class
        fields = [
            'id',
            'init',
            'end',
            'lesson',
            'state',
            'url',
            'user'
        ]


class ClassSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """Class sign up serializer.

    Handle sign up data validation and class creation.
    """

    id = serializers.ReadOnlyField()
    user_id = serializers.IntegerField(write_only=True)
    lesson_id = serializers.IntegerField(write_only=True)
    init = serializers.DateTimeField()
    end = serializers.DateTimeField()
    url = serializers.URLField()

    def validate(self, data):
        """Verify dates."""
        init = data['init']
        end = data['end']
        class_obj = Class.objects.filter(init__lte=init, end__gte=init, state=True, user_id=data['user_id']).first()
        if not class_obj is None:
            self.register_error(
                error_message='There is already a class registered for the teacher at the same time,Ya existe una clase registrada para el profesor en el mismo horario', error_code=8000)
        if init == end:
            self.register_error(
                error_message='The start and end date cannot be the same,La fecha de inicio y de finalizacion no pueden ser iguales', error_code=8000)
        if end < init:
            self.register_error(
                error_message='The end date and time cannot be less than the start date and time,La fecha y hora de finalización no puede ser menor a la fecha y hora de inicio', error_code=8000)
        return data

    def create(self, data):
        """Handle class creation."""
        class_obj = Class.objects.create(**data)
        return class_obj
