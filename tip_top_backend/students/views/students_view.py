# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.students.serializers import (
    StudentModelSerializer
)

# Model
from tip_top_backend.students.models import Student

# Permissions
from tip_top_backend.utils.permissions import AdminPermision
from rest_framework.permissions import (IsAuthenticated)


class StudentAPIView(APIView):
    """Student API view."""

    permission_classes = [IsAuthenticated, AdminPermision]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        if 'current_lesson' in request.GET:
            students = Student.objects.filter(current_lesson_id=request.GET['current_lesson'])
        if 'user' in request.GET:
            students = Student.objects.filter(user_id=request.GET['user'])
        else:
            students = Student.objects.all()
        serializer = StudentModelSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
