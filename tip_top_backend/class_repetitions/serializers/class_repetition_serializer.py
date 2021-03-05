"""ClassRepetition serializer."""

# Django REST framework
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Model
from tip_top_backend.class_repetitions.models import ClassRepetition


class ClassRepetitionModelSerializer(serializers.ModelSerializer):
    """ClassRepetition model serializer"""

    class Meta:
        """Meta class."""
        model = ClassRepetition
        fields = (
            'id',
            'last_repeat_date',
            'days'
        )


class ClassRepetitionSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """ClassRepetition sign up serializer.

    Handle sign up data validation and ClassRepetition creation.
    """

    id = serializers.ReadOnlyField()
    last_repeat_date = serializers.DateTimeField()
    days = serializers.ListField(child=serializers.BooleanField(default=False), allow_empty=False)

    def validate(self, data):
        """Verify dates."""
        days = data['days']
        if not any(days):
            self.register_error(
                error_message='You must select at least one day to repeat the class,Debe seleccionar al menos un día para repetir la clase', error_code=8000)
        return data

    def create(self, data):
        """Handle ClassRepetition creation."""
        class_repetition = ClassRepetition.objects.create(**data)
        return class_repetition
