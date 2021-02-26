# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.parents.serializers import (
    ParentModelSerializer
)

# Model
from tip_top_backend.parents.models import Parent

# Permissions
from tip_top_backend.utils.permissions import AdminPermision
from rest_framework.permissions import (IsAuthenticated)


class ParentAPIView(APIView):
    """Student API view."""

    # permission_classes = [IsAuthenticated, AdminPermision]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        if 'student' in request.GET:
            parents = Parent.objects.filter(student_id=request.GET['student'])
        else:
            parents = Parent.objects.all()
        serializer = ParentModelSerializer(parents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
