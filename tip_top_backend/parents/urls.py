"""Parents URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.parents.views import (
    ParentAPIView
)

urlpatterns = [
    path('api/parents/', ParentAPIView.as_view(), name='parents'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
