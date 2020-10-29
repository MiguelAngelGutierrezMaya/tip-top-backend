"""Classes URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.classes.views import (
    ClassAPIView
)

urlpatterns = [
    path('api/classes/', ClassAPIView.as_view(), name='classes'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
