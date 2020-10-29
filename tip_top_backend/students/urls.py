"""Students URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.students.views import (
    StudentAPIView
)

urlpatterns = [
    path('api/students/', StudentAPIView.as_view(), name='users'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
