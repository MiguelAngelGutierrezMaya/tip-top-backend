"""Lesson admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Lesson admin."""
    list_display = ('title', 'is_last', 'parent', 'unit', 'level')
    search_fields = ('title', 'is_last', 'parent', 'unit', 'level')
    list_filter = ('title', 'is_last', 'parent', 'unit', 'unit__level__name')

    def level(self, obj):
        return obj.unit.level

    level.admin_order_field = 'unit__level__name'
