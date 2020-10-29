"""Lessons URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.lessons.views import (
    LessonAPIView
)

urlpatterns = [
    path('api/lessons/', LessonAPIView.as_view(), name='lessons'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
