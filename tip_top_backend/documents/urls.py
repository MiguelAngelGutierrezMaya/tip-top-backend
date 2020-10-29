"""Documents URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.documents.views import (
    DocumentAPIView
)


urlpatterns = [
    path('api/documents/', DocumentAPIView.as_view(), name='documents'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
