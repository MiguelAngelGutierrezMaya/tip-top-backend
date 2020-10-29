"""Material URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.materials.views import (
    MaterialAPIView
)

urlpatterns = [
    path('api/materials/', MaterialAPIView.as_view(), name='lessons'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
