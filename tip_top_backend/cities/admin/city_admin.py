"""City admin."""

# Dependencies
import csv

# Django
from django.contrib import admin
from django.http import HttpResponse

# Models
from tip_top_backend.cities.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """City admin."""
    list_display = ('name', 'state',)
    search_fields = ('name', 'state',)
    list_filter = ('name', 'state',)
    actions = ["export_as_csv"]

    def has_delete_permission(self, request, obj=None):
        return False

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar seleccionados"
