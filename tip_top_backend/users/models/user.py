"""User model."""

# Dependencies
from datetime import datetime

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from tip_top_backend.utils.audit_model import AuditModel


class User(AuditModel, AbstractUser):
    """Users model.

    Extends from Django's AbstractUser, change the username field
    to email and add some extra fields."""

    first_name = models.CharField('Nombres', max_length=50, null=False, blank=False)
    last_name = models.CharField('Apellidos', max_length=80, null=False, blank=False)
    phone_number = models.CharField('Numero', max_length=20, null=False, blank=False)
    address = models.CharField('Direccion', max_length=100, null=False, blank=False)
    document_number = models.CharField('Documento', max_length=15, null=False, blank=False)
    email = models.EmailField('Email address', unique=True)
    admission_date = models.DateTimeField(default=datetime.now, blank=True)
    link = models.URLField('Enlace de videollamada', max_length=200, null=True, blank=True)

    # ManyToOne Relations
    role = models.ForeignKey('roles.Role', default=1, on_delete=models.CASCADE)
    document = models.ForeignKey('documents.Document', default=1, on_delete=models.CASCADE)
    city = models.ForeignKey('cities.City', default=1, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'document_number']

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
