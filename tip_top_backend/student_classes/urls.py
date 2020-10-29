"""StudentClasses URLs"""

# Django
from django.urls import path
from django.conf.urls import url

# Django REST framework
from rest_framework.urlpatterns import format_suffix_patterns

# Views
from tip_top_backend.student_classes.views import (
    StudentClassAPIView
)

urlpatterns = [
    path('api/student-classes/', StudentClassAPIView.as_view(), name='student-classes'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
