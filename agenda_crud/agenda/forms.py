from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, User
import re


# Formulario de registro de usuarios
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Formulario para crear/editar contactos
class ContactForm(forms.ModelForm):
    #class Meta:
    #    model = Contact
    #    fields = '__all__'  # Incluye todos los campos del modelo
    class Meta:
        model = Contact
        exclude = ['fecha_registro', 'creado_por', 'modificado_por']  # Excluye estos campos del formulario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza los campos si es necesario
        self.fields['nombres'].required = False
        self.fields['apellidos'].required = False
        self.fields['telefono'].required = False
        self.fields['email'].required = False
        self.fields['razon_social'].required = False
        self.fields['rut'].required = False
        self.fields['direccion'].required = False
        self.fields['numero_registro'].required = False  # Asegúrate de que sea opcional

    def clean_numero_registro(self):
        numero_registro = self.cleaned_data.get('numero_registro')
        if numero_registro and not re.match(r'^\d{4}-\d{3}$', numero_registro):
            raise forms.ValidationError('El número de registro debe tener el formato 0000-000.')
        return numero_registro