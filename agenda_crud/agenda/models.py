from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone

# Extender el modelo de usuario predeterminado
class User(AbstractUser):
    # Especifica un related_name único para los campos groups y user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="agenda_user_groups",  # related_name único
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="agenda_user_permissions",  # related_name único
        related_query_name="user",
    )

# Modelo para los contactos
from django.db import models
from django.core.exceptions import ValidationError
import re

class Contact(models.Model):
    numero_registro = models.CharField(
        max_length=8,
        unique=True,  # Asegura que no haya duplicados
        verbose_name="Número de Registro",
        help_text="Formato: 0000-000",
        blank=True,  # Permite que el campo esté vacío
        null=True,   # Permite valores nulos en la base de datos
    )
    nombres = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    apellidos = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Opcional
    email = models.EmailField(blank=True, null=True)  # Opcional
    razon_social = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    rut = models.CharField(max_length=12, blank=True, null=True)  # Opcional
    fecha_registro = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contactos_creados')
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contactos_modificados')
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)  # Opcional

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def clean(self):
        super().clean()
        # Validación del formato del número de registro
        if self.numero_registro and not re.match(r'^\d{4}-\d{3}$', self.numero_registro):
            raise ValidationError({
                'numero_registro': 'El número de registro debe tener el formato 0000-000.'
            })

    class Meta:
        ordering = ['-fecha_registro']