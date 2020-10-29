"""Memo serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.student_classes.serializers.student_class_serializer import StudentClassModelSerializer

# Model
from tip_top_backend.memos.models import Memo

# Utils
from tip_top_backend.utils.constants import Constants


class MemoModelSerializer(serializers.ModelSerializer):
    """Memo model serializer."""

    student_class = StudentClassModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Memo
        fields = [
            'id',
            'date',
            'vocabulary_learned',
            'sentences_learned',
            'comments',
            'student_class',
            'type'
        ]


class MemoSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """Memo sign up serializer.

    Handle sign up data validation and Memo creation.
    """

    student_class_id = serializers.IntegerField(write_only=True)
    class_obj_id = serializers.IntegerField(write_only=True)
    date = serializers.DateTimeField()
    vocabulary_learned = serializers.CharField(style={'type': 'textarea'})
    sentences_learned = serializers.CharField(style={'type': 'textarea'})
    comments = serializers.CharField(style={'type': 'textarea'})
    type = serializers.CharField()

    def validate(self, data):
        """Verify dates."""
        if data['type'] == Constants.PUBLIC:
            memo_obj = Memo.objects.filter(
                type=Constants.PUBLIC, student_class_id=data['student_class_id'], student_class__class_obj_id=data['class_obj_id']).first()
            if not memo_obj is None:
                self.register_error(
                    error_message='There is already a registered student memo for the selected class,Ya existe un memo del estudiante registrado para la clase seleccionada', error_code=8000)
        return data

    def create(self, data):
        """Handle memo creation."""
        data.pop('class_obj_id')
        memo_obj = Memo.objects.create(**data)
        return memo_obj
