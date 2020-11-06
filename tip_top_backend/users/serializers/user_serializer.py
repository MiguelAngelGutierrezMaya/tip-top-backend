"""User serializer."""

# Django
from django.contrib.auth import authenticate

# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

# Serializers
from tip_top_backend.roles.serializers.role_serializer import RoleModelSerializer
from tip_top_backend.documents.serializers.document_serializer import DocumentModelSerializer
from tip_top_backend.cities.serializers.city_serializer import CityModelSerializer

# Model
from tip_top_backend.users.models import User


class UserModelSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """User model serializer"""

    picture = serializers.CharField(source='profile.url')
    role = RoleModelSerializer(read_only=True)
    document = DocumentModelSerializer(read_only=True)
    city = CityModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'id',
            'picture',
            'is_active',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'document_number',
            'admission_date',
            'role',
            'document',
            'city',
            'link'
        )


class UserSignUpSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation and user creation.
    """

    id = serializers.ReadOnlyField()
    role_id = serializers.IntegerField(write_only=True)
    document_id = serializers.IntegerField(write_only=True)
    city_id = serializers.IntegerField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=80)
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=100)
    document_number = serializers.CharField(max_length=15)
    password = serializers.CharField(min_length=8, max_length=30)
    password_confirmation = serializers.CharField(min_length=8, max_length=30)
    username = serializers.CharField(min_length=5, max_length=20)
    link = serializers.CharField(allow_blank=True, allow_null=True, max_length=200)
    email = serializers.EmailField()
    admission_date = serializers.DateTimeField()

    def validate(self, data):
        """Verify password match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        user_email = User.objects.filter(email=data['email']).first()
        user_username = User.objects.filter(username=data['username']).first()
        if not user_email is None:
            self.register_error(
                error_message='Email already exist,El email ingresado ya existe', error_code=8000)
        if not user_username is None:
            self.register_error(
                error_message='Username already exist,El nombre de usuario ingresado ya existe', error_code=8000)
        if passwd != passwd_conf:
            self.register_error(
                error_message='Passwords does not match,Las contraseñas no coinciden', error_code=8000)
        return data

    def create(self, data):
        """Handle user creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_superuser=False, is_staff=False, is_active=True)
        return user


class UserLoginSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    """User login serializer

    Handle the login request data.
    """

    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            self.register_error(
                error_message='Invalid credentials,Credenciales inválidas', error_code=8000)
        if not user.is_active:
            self.register_error(error_message='User is not active,Usuario no está activo', error_code=8001)
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
