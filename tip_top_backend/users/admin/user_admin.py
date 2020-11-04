"""User admin."""

# Django
from django.contrib import admin

# Models
from tip_top_backend.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin."""
    list_display = ('first_name', 'last_name', 'username', 'document', 'city', 'role',)
    search_fields = ('first_name', 'last_name', 'username', 'document', 'city', 'role',)
    list_filter = ('first_name', 'last_name', 'username', 'document', 'city', 'role',)
    readonly_fields = ('password',)
