# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.cities.serializers import (
    CityModelSerializer
)

# Model
from tip_top_backend.cities.models import City

# Permissions
from rest_framework.permissions import (IsAuthenticated)


class CityAPIView(APIView):
    """City API view."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        cities = City.objects.all()
        serializer = CityModelSerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
