# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

# Serializers
from tip_top_backend.lessons.serializers import (
    LessonModelSerializer
)

# Model
from tip_top_backend.lessons.models import Lesson

# Permissions
from rest_framework.permissions import (IsAuthenticated)
from tip_top_backend.utils.permissions import PartialGetPermision


class LessonAPIView(APIView):
    """Lesson API view."""

    permission_classes = [IsAuthenticated, PartialGetPermision]
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    paginator.page_size = api_settings.PAGE_SIZE

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        if not 'unit_id' in request.GET:
            if 'title' in request.GET:
                lessons = Lesson.objects.filter(title__icontains=request.GET['title'])
            elif 'last_lesson' in request.GET:
                lessons = Lesson.objects.first()
            else:
                lessons = Lesson.objects.all()
        else:
            if 'title' in request.GET:
                lessons = Lesson.objects.filter(unit_id=request.GET['unit_id'], title__contains=request.GET['title'])
            else:
                lessons = Lesson.objects.filter(unit_id=request.GET['unit_id'])

        if 'not_paginate' in request.GET:
            if not 'many' in request.GET:
                serializer = LessonModelSerializer(lessons)
            else:
                serializer = LessonModelSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        result_page = self.paginator.paginate_queryset(lessons, request)
        serializer = LessonModelSerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = LessonModelSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = LessonModelSerializer(request.data).data
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """Handle HTTP PUT request."""
        lesson = Lesson.objects.get(id=request.data['id'])
        serializer = LessonModelSerializer(lesson, context={'request': request}, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
