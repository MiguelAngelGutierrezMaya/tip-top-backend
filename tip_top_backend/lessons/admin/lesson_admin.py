"""Lesson admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Lesson admin."""
    list_display = ('title', 'is_last', 'parent', 'unit')
    search_fields = ('title', 'is_last', 'parent', 'unit')
    list_filter = ('title', 'is_last', 'parent', 'unit')
