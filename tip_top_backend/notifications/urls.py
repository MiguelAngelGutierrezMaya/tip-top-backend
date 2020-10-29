"""Notifications URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.notifications.views import (
    NotificationView
)

urlpatterns = [
    path('api/notifications/', NotificationView.as_view(), name='notifications'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
