"""Level serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.levels.serializers.parent_serializer import ParentLevelModelSerializer

# Model
from tip_top_backend.levels.models import Level

# Utils
import tip_top_backend.utils.validations as validations


class LevelModelSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """Level model serializer."""

    parent = ParentLevelModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Level
        fields = [
            'id',
            'name',
            'is_last',
            'parent'
        ]

    def validate(self, data):
        """Check is_last."""
        obj = Level.objects.filter(is_last=True).first()
        validation = validations.validate_is_last(obj, self.context)
        if not validation:
            self.register_error(
                error_message='There is already a level marked as the last,Ya existe un nivel marcado como el último', error_code=8000)
        return data
