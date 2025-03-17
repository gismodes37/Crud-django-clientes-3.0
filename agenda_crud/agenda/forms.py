from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, Proveedor, PrecioProveedor, Producto, HistorialPrecio    # Asegúrate de importar HistorialPrecio
import re
from .models import Contact, ContactPDF
from .models import Categoria, Subcategoria




# Formulario de registro de usuarios
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Formulario para crear/editar contactos
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['fecha_registro', 'creado_por', 'modificado_por', 'numero_registro']

    def clean(self):
        cleaned_data = super().clean()
        nombres = cleaned_data.get('nombres')
        apellidos = cleaned_data.get('apellidos')

        # Verificar si ya existe un contacto con los mismos nombres y apellidos
        if nombres and apellidos:
            existing_contact = Contact.objects.filter(nombres=nombres, apellidos=apellidos).exclude(pk=self.instance.pk)
            if existing_contact.exists():
                raise forms.ValidationError("Ya existe un contacto con los mismos nombres y apellidos.")

        return cleaned_data



class ContactPDFForm(forms.ModelForm):
    class Meta:
        model = ContactPDF
        fields = ['pdf']
        


# Formulario de proveedores
class PrecioProveedorForm(forms.ModelForm):
    class Meta:
        model = PrecioProveedor
        fields = ['producto', 'proveedor', 'precio_costo', 'descuento']

    def clean_precio_costo(self):
        precio_costo = self.cleaned_data.get('precio_costo')
        if precio_costo and precio_costo < 0:
            raise forms.ValidationError('El precio de costo no puede ser negativo.')
        return precio_costo

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento and (descuento < 0 or descuento > 100):
            raise forms.ValidationError('El descuento debe estar entre 0% y 100%.')
        return descuento



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
        fields = ['codigo', 'numero_registro', 'nombre', 'stock', 'precio_neto', 'margen_venta', 'flete', 'subcategoria']
        


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['codigo', 'nombre', 'descripcion']
        
        

from django import forms
from .models import Subcategoria, Categoria

from django import forms
from .models import Subcategoria, Categoria

class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['codigo', 'nombre', 'descripcion', 'categoria']

    def __init__(self, *args, **kwargs):
        super(SubcategoriaForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()  # Asegura que el campo categoria tenga opciones válidas