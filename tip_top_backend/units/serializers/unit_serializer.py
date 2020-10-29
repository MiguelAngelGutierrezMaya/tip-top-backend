"""Units serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.levels.serializers.level_serializer import LevelModelSerializer
from tip_top_backend.levels.serializers.parent_serializer import ParentLevelModelSerializer

# Model
from tip_top_backend.units.models import Unit

# Utils
import tip_top_backend.utils.validations as validations


class UnitModelSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """Unit model serializer."""

    level = LevelModelSerializer(read_only=True)
    parent = ParentLevelModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Unit
        fields = [
            'id',
            'name',
            'is_last',
            'level',
            'parent'
        ]

    def validate(self, data):
        """Check is_last."""
        obj = Unit.objects.filter(level_id=self.context['request'].data['level_id'], is_last=True).first()
        validation = validations.validate_is_last(obj, self.context)
        if not validation:
            self.register_error(
                error_message='There is already a unit marked as the last,Ya existe una unidad marcada como la última', error_code=8000)
        return data

    def save(self):
        data = self.context['request'].data
        if not 'is_last' in data:
            data['is_last'] = False
        if not 'parent_id' in data:
            data['parent_id'] = None

        if self.context['request'].method == 'POST':
            Unit(name=data['name'], is_last=data['is_last'],
                 level_id=data['level_id'], parent_id=data['parent_id']).save()
        elif self.context['request'].method == 'PUT':
            Unit.objects.filter(pk=data['id']).update(
                name=data['name'], is_last=data['is_last'], level_id=data['level_id'], parent_id=data['parent_id'])
