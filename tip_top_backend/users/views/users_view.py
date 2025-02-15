"""Users views."""

# Python dependencies
import environ
import json

# Django
from django.dispatch import receiver
from django.urls import reverse

# Django conf
from django.conf import settings

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

# Serializers
from tip_top_backend.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    ProfileModelSerializer,
    ProfileSignUpSerializer
)
from tip_top_backend.students.serializers import (
    StudentModelSerializer,
    StudentSignUpSerializer
)
from tip_top_backend.parents.serializers import (
    ParentModelSerializer,
    ParentSignUpSerializer
)
from tip_top_backend.notifications.serializers import (
    NotificationSignUpSerializer
)

# Permissions
from rest_framework.permissions import (IsAuthenticated)
from tip_top_backend.utils.permissions import PartialPatchPermision

# Models
from tip_top_backend.users.models import User
from tip_top_backend.lessons.models import Lesson
from tip_top_backend.students.models import Student
from tip_top_backend.parents.models import Parent

# Utils
from tip_top_backend.utils.permissions import get_user_by_token
from tip_top_backend.utils.constants import Constants
import tip_top_backend.utils.permissions as utils_permissions

# Third libraries
from django_rest_passwordreset.signals import reset_password_token_created


class UserLoginAPIView(APIView):
    """User login API view."""

    def get(self, request, *args, **kwargs):
        user = utils_permissions.get_user_by_token(request)
        serializer = UserModelSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    """User API view."""

    permission_classes = [IsAuthenticated, PartialPatchPermision]
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    paginator.page_size = api_settings.PAGE_SIZE

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        if 'id' in request.GET:
            users = User.objects.filter(id=request.GET['id'])
        elif 'email' in request.GET:
            users = User.objects.filter(email__icontains=request.GET['email'])
        elif 'first_name' in request.GET:
            users = User.objects.filter(first_name__icontains=request.GET['first_name'])
            if not users:
                users = User.objects.filter(username__icontains=request.GET['first_name'])
        elif 'role_teacher' in request.GET:
            users = User.objects.filter(role__name=Constants.ROLE_TEACHER)
        else:
            users = User.objects.all()

        if 'not_paginate' in request.GET:
            serializer = UserModelSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        result_page = self.paginator.paginate_queryset(users, request)
        serializer = UserModelSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.role.name == Constants.ROLE_USER:
            request.data['user_id'] = user.id
            # request.data['current_lesson_id'] = Lesson.objects.order_by('id').first().id
            serializer = StudentSignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            student = serializer.save()
            for parent in request.data['parents']:
                parent['student_id'] = student.id
                serializer = ParentSignUpSerializer(data=parent)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            data = StudentModelSerializer(student).data
        else:
            data = UserModelSerializer(user).data
        request.data['user_id'] = user.id
        request.data['url'] = settings.DJANGO_MEDIA_URL + settings.MEDIA_URL + 'pictures/default.jpg'
        serializer = ProfileSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        """Handle HTTP PATCH request."""
        user = get_user_by_token(request)
        if 'modify_password' in request.data:
            if user.check_password(request.data['password']):
                user.set_password(request.data['new_password'])
            else:
                return Response("The current password in the database does not match the one sent,La contraseña actual en base de datos no coincide con la enviada", status=status.HTTP_400_BAD_REQUEST)
        else:
            user.city_id = request.data['city_id']
            user.document_id = request.data['document_id']
            user.document_number = request.data['document_number']
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.phone_number = request.data['phone_number']
            user.address = request.data['address']
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        """Handle HTTP PATCH request."""
        user = User.objects.get(pk=request.data['id'])

        duplicate_username = User.objects.filter(username=request.data['username']).exclude(username=user.username)
        if duplicate_username.count() > 0:
            return Response(
                "Username already exist,El nombre de usuario ingresado ya existe",
                status=status.HTTP_400_BAD_REQUEST)

        if 'password' in request.data:
            if request.data['password'] != request.data['password_confirmation']:
                return Response(
                    "Passwords does not match,Las contraseñas no coinciden",
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(request.data['password'])

        user.username = request.data['username']
        user.role_id = request.data['role_id']
        user.email = request.data['email']
        user.city_id = request.data['city_id']
        user.document_id = request.data['document_id']
        user.document_number = request.data['document_number']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.phone_number = request.data['phone_number']
        user.address = request.data['address']
        user.link = request.data['link']
        user.save()

        if user.role.name == Constants.ROLE_USER:
            student = Student.objects.get(user_id=user.id)
            student.teacher = request.data['teacher']
            student.current_lesson_id = request.data['current_lesson_id']
            student.genre = request.data['genre']
            student.save()
            for parent_data in request.data['parents']:
                parent = Parent.objects.get(student_id=student.id)
                parent.first_name = parent_data['first_name']
                parent.last_name = parent_data['last_name']
                parent.type_parent = parent_data['type_parent']
                parent.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    env = environ.Env()

    # Change password
    reset_password_token.user.set_password(env('DJANGO_NEW_PASSWORD'))
    reset_password_token.user.save()

    # Notification data
    data_obj = {
        "username": reset_password_token.user.username,
        "password": env('DJANGO_NEW_PASSWORD'),
        "url": env('DJANGO_APP_URL'),
        "type": "forgot-password"
    }

    serializer = NotificationSignUpSerializer(data={
        'type': 'EMAIL',
        'status': 'PENDING',
        'to': reset_password_token.user.email,
        'data': json.dumps(data_obj),
        'title': 'Recuperación de contraseña, Password recover',
        'template': 'email/forgot-password',
    })

    serializer.is_valid(raise_exception=True)
    serializer.save()
