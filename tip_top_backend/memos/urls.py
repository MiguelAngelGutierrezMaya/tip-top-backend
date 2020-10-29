"""Memos URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.memos.views import (
    MemoAPIView
)

urlpatterns = [
    path('api/memos/', MemoAPIView.as_view(), name='memos'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
