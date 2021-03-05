"""ClassRepetition views."""

# Python Dependencies
import datetime

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.class_repetitions.serializers import ClassRepetitionModelSerializer

# Tasks
from tip_top_backend.class_repetitions.tasks import class_repetition_cron


class ClassRepetitionAPIView(APIView):
    """ClassRepetition API View."""

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        try:
            class_repetitions = class_repetition_cron.generate_class_repetitions_service()
            serializer = ClassRepetitionModelSerializer(class_repetitions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
