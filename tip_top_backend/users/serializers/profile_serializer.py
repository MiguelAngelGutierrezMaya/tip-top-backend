"""User serializer."""

# Django
from django.contrib.auth import authenticate

# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.users.serializers.user_serializer import UserModelSerializer

# Model
from tip_top_backend.users.models import Profile


class ProfileModelSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """Profile model serializer"""

    user = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = Profile
        fields = (
            'id',
            'user',
            'url'
        )


class ProfileSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """Profile sign up serializer.

    Handle sign up data validation and profile creation.
    """

    user_id = serializers.IntegerField(write_only=True)
    url = serializers.URLField(max_length=200)

    def create(self, data):
        """Handle profile creation."""
        profile = Profile.objects.create(**data)
        return profile
