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
    class Meta:
        model = Contact
        fields = ['numero_registro', 'nombres', 'apellidos', 'telefono', 'email', 'razon_social', 'observaciones', 'pdf']

    def clean_numero_registro(self):
        numero_registro = self.cleaned_data.get('numero_registro')
        if not re.match(r'^\d{4}-\d{3}$', numero_registro):
            raise forms.ValidationError('El número de registro debe tener el formato 0000-000.')
        return numero_registro