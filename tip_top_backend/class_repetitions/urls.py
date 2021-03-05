"""StudentClasses URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.class_repetitions.views import ClassRepetitionAPIView

urlpatterns = [
    path('api/class-repetitions/', ClassRepetitionAPIView.as_view(), name='class-repetitions'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
