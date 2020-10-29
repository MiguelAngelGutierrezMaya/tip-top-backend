# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.documents.serializers import (
    DocumentModelSerializer
)

# Model
from tip_top_backend.documents.models import Document

# Permissions
from rest_framework.permissions import (IsAuthenticated)


class DocumentAPIView(APIView):
    """Document API view."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        documents = Document.objects.all()
        serializer = DocumentModelSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
