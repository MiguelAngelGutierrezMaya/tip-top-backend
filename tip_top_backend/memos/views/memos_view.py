"""Memo view"""

# Python dependencies
import json

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.memos.serializers import (
    MemoModelSerializer,
    MemoSignUpSerializer
)
from tip_top_backend.notifications.serializers import (
    NotificationSignUpSerializer
)

# Permissions
from rest_framework.permissions import (IsAuthenticated)

# Models
from tip_top_backend.memos.models import Memo

# Utils
from tip_top_backend.utils.constants import Constants


def saveNotification(request, serializer, memo_obj):
    request.data['title'] = 'Memo del estudiante'
    request.data['type'] = 'EMAIL'
    request.data['status'] = 'PENDING'
    request.data['to'] = memo_obj.student_class.student.user.email
    request.data['data'] = json.dumps({
        "type": "assignment",
        "student": f"{memo_obj.student_class.student.user.first_name} {memo_obj.student_class.student.user.last_name}",
        "date": serializer.data['date'],
        "vocabulary_learned": serializer.data['vocabulary_learned'],
        "sentences_learned": serializer.data['sentences_learned'],
        "comments": serializer.data['comments']
    })
    request.data['template'] = 'email/memo'
    serializer = NotificationSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()


class MemoAPIView(APIView):
    """Memo API view."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        memos = Memo.objects.filter(student_class__class_obj_id=request.GET['class_id'])
        serializer = MemoModelSerializer(memos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = MemoSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        memo_obj = serializer.save()
        if request.data['type'] == Constants.PUBLIC:
            saveNotification(request, serializer, memo_obj)
        data = MemoModelSerializer(memo_obj).data
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        """Handle HTTP PATCH request."""
        if request.data['type'] == Constants.PUBLIC:
            memo_obj = Memo.objects.filter(
                type=Constants.PUBLIC, student_class_id=request.data['student_class_id'], student_class__class_obj_id=request.data['class_obj_id']).first()
            if not memo_obj is None:
                return Response('There is already a public registered student memo for the selected class,Ya existe un memo público del estudiante registrado para la clase seleccionada', status=status.HTTP_400_BAD_REQUEST)
        memo = Memo.objects.get(pk=request.data['id'])
        memo.student_class_id = request.data['student_class_id']
        memo.date = request.data['date']
        memo.vocabulary_learned = request.data['vocabulary_learned']
        memo.sentences_learned = request.data['sentences_learned']
        memo.comments = request.data['comments']
        memo.type = request.data['type']
        memo.save()
        if request.data['type'] == Constants.PUBLIC:
            request.data['date'] = memo.date
            saveNotification(request, request, memo)
        return Response(status=status.HTTP_204_NO_CONTENT)
