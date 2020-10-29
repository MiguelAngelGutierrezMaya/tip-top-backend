"""Levels views."""

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

# Serializers
from tip_top_backend.levels.serializers import (
    LevelModelSerializer
)

# Model
from tip_top_backend.levels.models import Level

# Permissions
from rest_framework.permissions import (IsAuthenticated)
from tip_top_backend.utils.permissions import PartialGetPermision


class LevelAPIView(APIView):
    """Level API view."""

    permission_classes = [IsAuthenticated, PartialGetPermision]
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    paginator.page_size = api_settings.PAGE_SIZE

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        levels = Level.objects.all()
        result_page = self.paginator.paginate_queryset(levels, request)
        serializer = LevelModelSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = LevelModelSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        level = serializer.save()
        data = LevelModelSerializer(level).data
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """Handle HTTP PUT request."""
        level = Level.objects.get(id=request.data['id'])
        serializer = LevelModelSerializer(level, context={'request': request}, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
