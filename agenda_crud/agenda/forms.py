from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, User

# Formulario de registro de usuarios
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Formulario para crear/editar contactos
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nombres', 'apellidos', 'telefono', 'email', 'razon_social', 'observaciones']