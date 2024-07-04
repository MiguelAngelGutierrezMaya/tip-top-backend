# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.student_classes.serializers import (
    StudentClassModelSerializer
)

# Model
from tip_top_backend.student_classes.models import StudentClass
from tip_top_backend.students.models import Student

# Permissions
from rest_framework.permissions import (IsAuthenticated)

# Utils
from tip_top_backend.utils.permissions import get_user_by_token
from tip_top_backend.utils.constants import Constants


class StudentClassAPIView(APIView):
    """StudentClass API view."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        user = get_user_by_token(request)
        print('user', user, user.role.name, request.GET)
        if 'class_id' in request.GET and user.role.name != Constants.ROLE_USER:
            data = StudentClass.objects.filter(class_obj_id=request.GET['class_id'])
        elif user.role.name == Constants.ROLE_ADMIN:
            data = StudentClass.objects.select_related('class_obj').filter(
                class_obj__init__gte=request.GET['init'], class_obj__end__lte=request.GET['end'])
        elif user.role.name == Constants.ROLE_TEACHER:
            data = StudentClass.objects.select_related('class_obj').filter(
                class_obj__init__gte=request.GET['init'], class_obj__end__lte=request.GET['end'], class_obj__user_id=user.id)
        else:
            student = Student.objects.filter(user_id=user.id).first()
            data = StudentClass.objects.filter(student_id=student.id).select_related('class_obj').filter(
                class_obj__init__gte=request.GET['init'], class_obj__end__lte=request.GET['end'])
        serializer = StudentClassModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        return Response(None, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """Handle HTTP PUT request."""
        return Response(status=status.HTTP_204_NO_CONTENT)
