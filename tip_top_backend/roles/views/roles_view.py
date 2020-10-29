# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.roles.serializers import (
    RoleModelSerializer
)

# Model
from tip_top_backend.roles.models import Role

# Permissions
from rest_framework.permissions import (IsAuthenticated)
from tip_top_backend.utils.permissions import AdminPermision


class RoleAPIView(APIView):
    """Role API view."""

    permission_classes = [IsAuthenticated, AdminPermision]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        roles = Role.objects.all()
        serializer = RoleModelSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
