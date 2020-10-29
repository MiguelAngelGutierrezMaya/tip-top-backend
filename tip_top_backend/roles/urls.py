"""Roles URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.roles.views import (
    RoleAPIView
)


urlpatterns = [
    path('api/roles/', RoleAPIView.as_view(), name='roles'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
