"""Lessons serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.lessons.serializers.parent_serializer import ParentLessonModelSerializer
from tip_top_backend.units.serializers.unit_serializer import UnitModelSerializer

# Model
from tip_top_backend.lessons.models import Lesson

# Utils
import tip_top_backend.utils.validations as validations


class LessonModelSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """Lesson model serializer."""

    unit = UnitModelSerializer(read_only=True)
    parent = ParentLessonModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Lesson
        fields = [
            'id',
            'title',
            'is_last',
            'unit',
            'parent'
        ]

    def validate(self, data):
        """Check is_last."""
        obj = Lesson.objects.filter(unit_id=self.context['request'].data['unit_id'], is_last=True).first()
        validation = validations.validate_is_last(obj, self.context)
        if not validation:
            self.register_error(
                error_message='There is already a lesson marked as the last,Ya existe una lección marcada como la última', error_code=8000)
        return data

    def save(self):
        data = self.context['request'].data
        if not 'is_last' in data:
            data['is_last'] = False
        if not 'parent_id' in data:
            data['parent_id'] = None

        if self.context['request'].method == 'POST':
            Lesson(title=data['title'], is_last=data['is_last'],
                   unit_id=data['unit_id'], parent_id=data['parent_id']).save()
        elif self.context['request'].method == 'PUT':
            Lesson.objects.filter(pk=data['id']).update(
                title=data['title'], is_last=data['is_last'], unit_id=data['unit_id'], parent_id=data['parent_id'])
