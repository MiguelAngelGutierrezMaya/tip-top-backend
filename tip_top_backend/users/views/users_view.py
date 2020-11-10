"""Users views."""

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

# Permissions
from rest_framework.permissions import (IsAuthenticated)
from tip_top_backend.utils.permissions import PartialPatchPermision

# Models
from tip_top_backend.users.models import User
from tip_top_backend.lessons.models import Lesson

# Utils
from tip_top_backend.utils.permissions import get_user_by_token
from tip_top_backend.utils.constants import Constants
import tip_top_backend.utils.permissions as utils_permissions


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
        if 'email' in request.GET:
            users = User.objects.filter(email=request.GET['email'])
        elif 'first_name' in request.GET:
            # users = User.objects.filter(first_name__contains=request.GET['first_name'])
            users = User.objects.filter(first_name__istartswith=request.GET['first_name'])
            if not users:
                users = User.objects.filter(username__istartswith=request.GET['first_name'])
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
            request.data['current_lesson_id'] = Lesson.objects.order_by('id').first().id
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
