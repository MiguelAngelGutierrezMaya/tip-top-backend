"""Units URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.units.views import (
    UnitAPIView
)


urlpatterns = [
    path('api/units/', UnitAPIView.as_view(), name='units'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
