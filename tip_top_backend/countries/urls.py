"""Countries URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = []

urlpatterns = format_suffix_patterns(urlpatterns)
