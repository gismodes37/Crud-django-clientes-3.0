from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, Proveedor, PrecioProveedor, Producto
import re


# Formulario de registro de usuarios
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Formulario para crear/editar contactos
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['fecha_registro', 'creado_por', 'modificado_por', 'numero_registro']  # Excluir numero_registro para que se genere automáticamente

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer el campo "id" de solo lectura si el objeto ya existe
        if self.instance and self.instance.id:
            self.fields['id'] = forms.IntegerField(
                initial=self.instance.id,  # Valor inicial del campo
                widget=forms.TextInput(attrs={'readonly': 'readonly'}),  # Hacer el campo de solo lectura
                label="ID"  # Etiqueta del campo
            )
        
        # Hacer otros campos opcionales (esto no cambia)
        self.fields['nombres'].required = False
        self.fields['apellidos'].required = False
        self.fields['telefono'].required = False
        self.fields['email'].required = False
        self.fields['razon_social'].required = False
        self.fields['rut'].required = False
        self.fields['direccion'].required = False


# Formulario de proveedores
class PrecioProveedorForm(forms.ModelForm):
    class Meta:
        model = PrecioProveedor
        fields = ['producto', 'proveedor', 'precio_costo']


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['codigo', 'nombre', 'raz_social', 'rut_p', 'contacto', 'telefono', 'email', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].required = True
        self.fields['nombre'].required = True
        self.fields['raz_social'].required = True
        self.fields['rut_p'].required = True
        self.fields['contacto'].required = True

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not re.match(r'^\+?1?\d{9,15}$', telefono):
            raise forms.ValidationError('El número de teléfono debe tener un formato válido.')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError('Ingrese un correo electrónico válido.')
        return email


# Formulario de productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'numero_registro', 'nombre', 'stock', 'precio_neto', 'margen_venta', 'flete', 'subfamilia']