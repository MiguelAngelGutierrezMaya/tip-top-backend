"""Country admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.countries.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Country admin."""

    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
