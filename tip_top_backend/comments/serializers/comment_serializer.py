"""Comment serializer."""

# Django REST framework
from rest_framework import serializers

# Serializers
from tip_top_backend.lessons.serializers.lesson_serializer import LessonModelSerializer

# Model
from tip_top_backend.comments.models import Comment


class CommentModelSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    lesson = LessonModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Comment
        fields = [
            'title',
            'content',
            'date',
            'lesson'
        ]
