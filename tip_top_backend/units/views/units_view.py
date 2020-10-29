# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

# Serializers
from tip_top_backend.units.serializers import (
    UnitModelSerializer
)

# Model
from tip_top_backend.units.models import Unit

# Permissions
from rest_framework.permissions import (IsAuthenticated)
from tip_top_backend.utils.permissions import PartialGetPermision


class UnitAPIView(APIView):
    """Unit API view."""

    permission_classes = [IsAuthenticated, PartialGetPermision]
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    paginator.page_size = api_settings.PAGE_SIZE

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        if not 'level_id' in request.GET:
            units = Unit.objects.all()
        else:
            units = Unit.objects.filter(level_id=request.GET['level_id'])

        if 'not_paginate' in request.GET:
            serializer = UnitModelSerializer(units, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        result_page = self.paginator.paginate_queryset(units, request)
        serializer = UnitModelSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UnitModelSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        unit = serializer.save()
        data = UnitModelSerializer(request.data).data
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """Handle HTTP PUT request."""
        unit = Unit.objects.get(id=request.data['id'])
        serializer = UnitModelSerializer(unit, context={'request': request}, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
