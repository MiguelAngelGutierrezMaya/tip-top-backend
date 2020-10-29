"""Cities URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.cities.views import (
    CityAPIView
)


urlpatterns = [
    path('api/cities/', CityAPIView.as_view(), name='cities'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
