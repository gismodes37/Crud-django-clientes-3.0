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
    rut = models.CharField(
        max_length=12, 
        blank=True, 
        null=True, 
        help_text="Formato: 00.000.000-0", 
        verbose_name="Número de Rut"
    )  # Opcional
    direccion = models.CharField(max_length=100, blank=True, null=True)  # Opcional
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
        

#---------------------*---------------------#  
#from .forms import ProveedorForm
#from .models import Producto

      
# Modelo de Proveedores
class Familia(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"



class SubFamilia(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='subfamilias')

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.familia.nombre})"
    
    

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, default="CODIGO_TEMPORAL")  # Valor predeterminado
    numero_registro = models.CharField(max_length=50, unique=True, default="TEMPORAL")  # Valor predeterminado
    nombre = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()
    precio_neto = models.DecimalField(max_digits=10, decimal_places=2)
    margen_venta = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    flete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subfamilia = models.ForeignKey(SubFamilia, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"  # Asegurar que el código aparece en la representación


class Proveedor(models.Model):
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código de Proveedor")
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    raz_social = models.CharField(max_length=100, blank=True, null=True)
    rut_p = models.CharField(
        max_length=12, 
        blank=True, 
        null=True, 
        help_text="Formato: 00.000.000-0", 
        verbose_name="Número de Rut"
    )  # Opcional
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='proveedores_creados')
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='proveedores_modificados')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    

# Relación Producto-Proveedor con precios y descuento
class PrecioProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Descuento en porcentaje
    fecha_actualizacion = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('producto', 'proveedor')  # Evita duplicados

    @property
    def precio_con_descuento(self):
        """Calcula el precio de costo con descuento aplicado."""
        return self.precio_costo * (1 - (self.descuento / 100))

    def __str__(self):
        return f"{self.proveedor.nombre} - {self.producto.nombre}: ${self.precio_con_descuento} (Descuento: {self.descuento}%)"


    
    


