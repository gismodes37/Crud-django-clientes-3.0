from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
import os  # 👈 Agrega esta línea


# Extender el modelo de usuario predeterminado
class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="agenda_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="agenda_user_permissions",
        related_query_name="user",
    )

# Modelo para los contactos
from django.db import models
from django.core.exceptions import ValidationError
import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify




class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    numero_registro = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="Número de Registro",
        help_text="Formato: 0000-000",
        blank=True,
        null=True
    )
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    razon_social = models.CharField(max_length=100, blank=True, null=True)
    rut = models.CharField(
        max_length=12, 
        blank=True, 
        null=True, 
        help_text="Formato: 00.000.000-0", 
        verbose_name="Número de Rut"
    )
    direccion = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contactos_creados')
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contactos_modificados')
    #pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.numero_registro:
            self.numero_registro = f"{timezone.now().year}-{self.id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_registro} - {self.nombres} {self.apellidos}"

    class Meta:
        ordering = ['-fecha_registro']
        unique_together = ['nombres', 'apellidos']  # 👈 Restricción única para nombres y apellidos
        
        
        

class ContactPDF(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='pdfs')
    pdf = models.FileField(upload_to='pdfs/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
    # Verificar si el archivo ya tiene un nombre asignado
        if self.pdf and not self.pk:  # Solo si es un nuevo archivo
        # Obtener el nombre original del archivo
            original_name = os.path.basename(self.pdf.name)
        
        # Tomar los primeros 8 caracteres del nombre original
            short_name = original_name[:8]
        
        # Obtener la extensión del archivo
            extension = os.path.splitext(original_name)[1]  # Obtener la extensión
        
        # Agregar el ID del contacto para evitar colisiones
            unique_name = f"{self.contact.id}_{short_name}{extension}"
        
        # Renombrar el archivo
            self.pdf.name = f"pdfs/{unique_name}"
    
    # Guardar el objeto
        super().save(*args, **kwargs)
    
    
    

# Señal para generar el numero_registro después de guardar el objeto
@receiver(post_save, sender=Contact)
def generar_numero_registro(sender, instance, created, **kwargs):
    if created and not instance.numero_registro:
        instance.numero_registro = f"{timezone.now().year}-{instance.id:03d}"
        instance.save()

        
    
# Modelo de Proveedores
class Categoria(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'agenda_categorias'  # Especifica el nombre de la tabla

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    

class Subcategoria(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')

    class Meta:
        db_table = 'agenda_subcategorias'  # Especifica el nombre de la tabla

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.categoria.nombre})"
    
    

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, default="CODIGO_TEMPORAL")  # Valor predeterminado
    numero_registro = models.CharField(max_length=50, unique=True, default="TEMPORAL")  # Valor predeterminado
    nombre = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()
    precio_neto = models.DecimalField(max_digits=10, decimal_places=2)
    margen_venta = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    flete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, related_name='productos')  # Aquí corregimos a "Subcategoria"

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


    
class HistorialPrecio(models.Model):
    precio_proveedor = models.ForeignKey(PrecioProveedor, on_delete=models.CASCADE)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.precio_proveedor} - {self.fecha_cambio}"

