"""Level admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.levels.models import Level


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    """Level admin."""
    list_display = ('name', 'is_last', 'parent',)
    search_fields = ('name', 'is_last', 'parent',)
    list_filter = ('name', 'is_last', 'parent',)
