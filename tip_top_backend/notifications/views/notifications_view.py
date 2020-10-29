"""Users views."""

# Python Dependencies
import datetime

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

# Serializers
from tip_top_backend.notifications.serializers import (
    NotificationModelSerializer,
    NotificationSignUpSerializer
)
from tip_top_backend.user_notifications.serializers import (
    UserNotificationModelSerializer,
    UserNotificationSignUpSerializer
)

# Models
from tip_top_backend.notifications.models import Notification
from tip_top_backend.classes.models import Class

# Permissions
from tip_top_backend.utils.permissions import PartialGetPermisionAdminTeacher

# Utils
from tip_top_backend.utils.permissions import get_user_by_token

# Tasks
from tip_top_backend.notifications.tasks import send_notifications_cron


class NotificationView(APIView):
    """User sign up API View."""

    permission_classes = [PartialGetPermisionAdminTeacher]
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    paginator.page_size = api_settings.PAGE_SIZE - 2

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        if request.data['type'] == 'PRIVATE':
            class_obj = Class.objects.get(pk=request.data['class_id'])
            current_date = (datetime.datetime.now() - datetime.timedelta(hours=5))
            if current_date < class_obj.init:
                return Response("You cannot report a student's absence to a class that has not started,No puedes notificar la inasistencia de un estudiante a un clase que no ha comenzado", status=status.HTTP_400_BAD_REQUEST)

        serializer = NotificationSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = get_user_by_token(request)
        request.data['date'] = datetime.datetime.now()
        request.data['user_id'] = user.id
        request.data['notification_id'] = serializer.data['id']

        serializer = UserNotificationSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        try:
            if 'admin_notifications' in request.GET:
                notifications = Notification.objects.filter(type='PRIVATE')
            else:
                data = send_notifications_cron.notification_service()
                return Response(data, status=status.HTTP_200_OK)
            result_page = self.paginator.paginate_queryset(notifications, request)
            serializer = NotificationModelSerializer(result_page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
