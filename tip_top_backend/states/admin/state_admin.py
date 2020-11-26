"""State admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.states.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """State admin."""
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    list_filter = ('name', 'country')

    def has_delete_permission(self, request, obj=None):
        return False
