"""Unit admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.units.models import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Unit admin."""
    list_display = ('name', 'is_last', 'parent', 'level')
    search_fields = ('name', 'is_last', 'parent', 'level')
    list_filter = ('name', 'is_last', 'parent', 'level')
