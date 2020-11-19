"""Countries URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.countries.views import (
    CountryAPIView
)

urlpatterns = [
    path('api/countries/', CountryAPIView.as_view(), name='countries'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
