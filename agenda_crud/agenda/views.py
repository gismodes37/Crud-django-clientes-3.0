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
from django.core.exceptions import FieldError

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
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        raw_data = csv_file.read()

        # Forzar decodificación en UTF-8
        try:
            file_content = raw_data.decode('utf-8', errors='replace').splitlines()
        except UnicodeDecodeError:
            messages.error(request, 'Error: No se pudo decodificar el archivo CSV en UTF-8.')
            return redirect('upload_csv')

        csv_reader = csv.DictReader(file_content)
        print("Cabeceras detectadas:", csv_reader.fieldnames)

        required_columns = {'Número de Registro', 'Nombres', 'Apellidos', 'Teléfono', 'Email', 'Razón Social', 'Rut'}
        if not required_columns.issubset(csv_reader.fieldnames):
            messages.error(request, 'El archivo CSV no tiene el formato correcto.')
            print("ERROR: Cabeceras incorrectas:", csv_reader.fieldnames)
            return redirect('upload_csv')

        print("Contenido del archivo CSV:")
        registros_creados = 0

        for row in csv_reader:
            row = {k: v if v is not None else '' for k, v in row.items()}  # 👈 Convierte None en ''

            print(row)  # 👈 Verifica que las filas sean correctas

            numero_registro = row.get('Número de Registro', '').strip()

            if Contact.objects.filter(numero_registro=numero_registro).exists():
                continue  # Si ya existe, saltar al siguiente

            try:
                contacto = Contact(
                    numero_registro=numero_registro or None,
                    nombres=row.get('Nombres', '').strip() or None,
                    apellidos=row.get('Apellidos', '').strip() or None,
                    telefono=row.get('Teléfono', '').strip() or None,
                    email=row.get('Email', '').strip() or None,
                    razon_social=row.get('Razón Social', '').strip() or None,
                    rut=row.get('Rut', '').strip() or None,  # 👈 Ahora ya no dará error
                    creado_por=request.user,
                    modificado_por=request.user
                )
                contacto.full_clean()
                contacto.save()
                registros_creados += 1
            except (KeyError, ValidationError) as e:
                print(f"Error en {numero_registro}: {e}")

        messages.success(request, f'Se importaron {registros_creados} nuevos contactos.')
        return redirect('contact_list')

    return render(request, 'agenda/upload_csv.html')





# Vista para descargar contactos como CSV
@user_passes_test(es_administrador, login_url='/accounts/login/')
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contactos.csv"'

    writer = csv.writer(response)
    # Agregar la cabecera del CSV
    writer.writerow(['Número de Registro', 'Nombres', 'Apellidos', 'Teléfono', 'Email', 'Razón Social', 'Rut'])

    # Ordenar los contactos por número de registro antes de exportar
    contactos = Contact.objects.all().order_by('numero_registro')

    for contacto in contactos:
        writer.writerow([
            contacto.numero_registro or "",  
            contacto.nombres or "",
            contacto.apellidos or "",
            contacto.telefono or "",
            contacto.email or "",
            contacto.razon_social or "",
            contacto.rut or ""
        ])

    return response



# Listado de contactos
@login_required
def contact_list(request):
    query = request.GET.get('q', '')  # Parámetro de búsqueda
    order_by = request.GET.get('order_by', 'numero_registro')  # Columna de ordenación
    order = request.GET.get('order', 'asc')  # Orden (asc o desc)

    # Aplicar el orden
    if order == 'desc':
        order_by = f'-{order_by}'  # Agregar un guion para orden descendente
    else:
        order_by = f'{order_by}'  # Mantener orden ascendente

    # Obtener todos los registros ordenados antes de la paginación
    try:
        contacts = Contact.objects.all().order_by(order_by)
    except FieldError:
        contacts = Contact.objects.all().order_by('numero_registro')

    # Filtrar por búsqueda si hay un query
    if query:
        contacts = contacts.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query) |
            Q(razon_social__icontains=query)
        )

    # Aplicar paginación
    paginator = Paginator(contacts, 10)  # 10 registros por página
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'agenda/contact_list.html', {
        'contacts': contacts,
        'query': query,
        'order_by': request.GET.get('order_by', 'numero_registro'),  # Mantener la clave correcta en la URL
        'order': order,
    })



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
