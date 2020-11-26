"""Level admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Level admin."""
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

    def has_delete_permission(self, request, obj=None):
        return False
