# Python dependencies
import os
import uuid

# Django conf
from django.conf import settings

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

# Serializers
from tip_top_backend.materials.serializers import (
    MaterialModelSerializer,
    MaterialSignUpSerializer
)

# Model
from tip_top_backend.materials.models import Material

# Permissions
from rest_framework.permissions import (IsAuthenticated)


class MaterialAPIView(APIView):
    """Material API view."""

    permission_classes = [IsAuthenticated]
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    paginator.page_size = api_settings.PAGE_SIZE - 3

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        materials = Material.objects.filter(lesson_id=request.GET['lesson_id'])
        if 'not_paginate' in request.GET:
            serializer = MaterialModelSerializer(materials, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        result_page = self.paginator.paginate_queryset(materials, request)
        serializer = MaterialModelSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        file_array = request.FILES['file'].name.split('.')
        filename = str(uuid.uuid1()) + '.' + file_array[len(file_array) - 1]
        path = '/materials/' + filename

        with open(settings.MEDIA_ROOT + path, 'wb+') as destination:
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)

        request.data['url'] = settings.DJANGO_MEDIA_URL + settings.MEDIA_URL + path[1:len(path)]
        request.data['name'] = request.FILES['file'].name
        request.data['type'] = file_array[len(file_array) - 1]
        serializer = MaterialSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        material = serializer.save()
        data = MaterialModelSerializer(material).data
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Handle HTTP DELETE request."""
        try:
            material = Material.objects.get(pk=request.data['id'])
            file_array = material.url.split('/')
            filename = file_array[len(file_array) - 1]
            path = 'materials/' + filename
            os.remove(os.path.join(settings.MEDIA_ROOT, path))
            material.delete()
        except:
            pass
        return Response(None, status=status.HTTP_204_NO_CONTENT)
