# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.countries.serializers import (
    CountryModelSerializer
)

# Model
from tip_top_backend.countries.models import Country

# Permissions
from rest_framework.permissions import (IsAuthenticated)


class CountryAPIView(APIView):
    """Country API view."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        countries = Country.objects.all()
        serializer = CountryModelSerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
