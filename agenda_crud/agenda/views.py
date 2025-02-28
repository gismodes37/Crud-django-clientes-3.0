from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import csv
import chardet

from .models import Contact
from .forms import UserRegisterForm, ContactForm

# Función para verificar si el usuario es administrador
def es_administrador(user):
    return user.is_authenticated and user.is_staff

# Vista de inicio
def home(request):
    user_name = request.user.username if request.user.is_authenticated else "Invitado"
    return render(request, 'agenda/home.html', {'user_name': user_name})

# Vista de inicio de sesión personalizada
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Hola, {user.username}! Bienvenido de nuevo.')
            return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'registration/login.html')

# Vista de registro de usuarios
@user_passes_test(es_administrador, login_url='/accounts/login/')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'¡Usuario {user.username} creado exitosamente!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Vista para subir un archivo CSV
@user_passes_test(es_administrador, login_url='/accounts/login/')
def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        raw_data = csv_file.read()

        # Detectar codificación
        encoding = chardet.detect(raw_data)['encoding']
        try:
            file_content = raw_data.decode(encoding).splitlines()
        except UnicodeDecodeError:
            messages.error(request, 'Error: No se pudo decodificar el archivo CSV.')
            return redirect('upload_csv')

        csv_reader = csv.DictReader(file_content)
        required_columns = {'Nombres', 'Apellidos', 'Teléfono', 'Email', 'Razón Social', 'Rut'}

        if not required_columns.issubset(csv_reader.fieldnames):
            messages.error(request, 'El archivo CSV no tiene el formato correcto.')
            return redirect('upload_csv')

        for row in csv_reader:
            try:
                contacto = Contact(
                    nombres=row['Nombres'],
                    apellidos=row['Apellidos'],
                    telefono=row['Teléfono'],
                    email=row['Email'],
                    razon_social=row['Razón Social'],
                    rut=row['Rut'],
                    creado_por=request.user,
                        modificado_por=request.user,  # ← Asigna el usuario que lo modifica

                )
                contacto.full_clean()
                contacto.save()
            except (KeyError, ValidationError) as e:
                messages.error(request, f'Error en el archivo CSV: {e}')
                return redirect('upload_csv')

        messages.success(request, 'Archivo CSV subido y procesado correctamente.')
        return redirect('contact_list')
    
    return render(request, 'agenda/upload_csv.html')

# Vista para descargar contactos como CSV
@user_passes_test(es_administrador, login_url='/accounts/login/')
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contactos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombres', 'Apellidos', 'Teléfono', 'Email', 'Razón Social', 'Rut'])
    for contacto in Contact.objects.all():
        writer.writerow([contacto.nombres, contacto.apellidos, contacto.telefono, contacto.email, contacto.razon_social, contacto.rut])
    return response

# Listado de contactos
@login_required
def contact_list(request):
    query = request.GET.get('q', '')
    contacts = Contact.objects.all()
    if query:
        contacts = contacts.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query) |
            Q(razon_social__icontains=query)
        )
    paginator = Paginator(contacts, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        contacts = paginator.page(1)
    return render(request, 'agenda/contact_list.html', {'contacts': contacts, 'query': query})



# Búsqueda de contactos en AJAX
def buscar_contactos(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'html': '<p>Ingresa al menos 2 caracteres para buscar.</p>'})
    
    contacts = Contact.objects.filter(
        Q(nombres__icontains=query) |
        Q(apellidos__icontains=query) |
        Q(telefono__icontains=query) |
        Q(email__icontains=query) |
        Q(razon_social__icontains=query)
    )
    html = render_to_string('agenda/partials/contactos_tabla.html', {'contacts': contacts})
    return JsonResponse({'html': html})



# CRUD de Contactos
@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'agenda/contact_detail.html', {'contact': contact})



@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES si hay archivos
        if form.is_valid():
            contact = form.save(commit=False)
            contact.creado_por = request.user  # Asigna el usuario que crea el contacto
            contact.save()  # Guarda el contacto en la base de datos
            return redirect('contact_list')  # Redirige a la lista de contactos después de guardar
        else:
            # Si el formulario no es válido, muestra los errores en la plantilla
            print("Errores en el formulario:", form.errors)  # Depuración: imprime errores en la consola
    else:
        form = ContactForm()  # Muestra un formulario vacío para GET requests

    return render(request, 'agenda/contact_form.html', {'form': form})



@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.modificado_por = request.user  # Asigna el usuario que realiza la modificación
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'agenda/contact_form.html', {'form': form})



@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'agenda/contact_confirm_delete.html', {'contact': contact})



# Logout personalizado
class CustomLogoutView(LogoutView):
    template_name = './registration/cerrar_sesion.html'
