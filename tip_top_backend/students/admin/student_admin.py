"""Student admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.students.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Student admin."""
    list_display = ('user', 'current_lesson',)
    search_fields = ('user', 'current_lesson',)
    list_filter = ('user', 'current_lesson',)
