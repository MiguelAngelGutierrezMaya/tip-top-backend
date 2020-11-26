"""City admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.cities.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """City admin."""
    list_display = ('name', 'state',)
    search_fields = ('name', 'state',)
    list_filter = ('name', 'state',)

    def has_delete_permission(self, request, obj=None):
        return False
