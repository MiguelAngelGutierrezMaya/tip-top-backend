"""Levels URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.levels.views import (
    LevelAPIView
)


urlpatterns = [
    path('api/levels/', LevelAPIView.as_view(), name='levels'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
