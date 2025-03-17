from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
from .views import (
    register, custom_login, buscar_global, contact_detail,
    upload_csv, download_csv,
    contact_list, contact_create, contact_update, contact_delete,
    producto_list, producto_create, producto_detail, producto_update, producto_delete,
    proveedor_list, proveedor_create, proveedor_detail, proveedor_update, proveedor_delete,
    precio_proveedor_list, precio_proveedor_create, precio_proveedor_update, precio_proveedor_delete,
    buscar_contactos, autocompletar, upload_pdf, delete_pdf,  # 👈 Agregar delete_pdf
    # Nuevas vistas para Categorías y Subcategorías
    categoria_list, categoria_create, categoria_update, categoria_delete,
    subcategoria_list, subcategoria_create, subcategoria_update, subcategoria_delete
)

# URLs para contactos
contact_urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='contact_create'),
    path('<int:pk>/edit/', views.contact_update, name='contact_update'),
    path('<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('<int:pk>/', views.contact_detail, name='contact_detail'),
    path('<int:pk>/upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('pdf/<int:pdf_id>/delete/', views.delete_pdf, name='delete_pdf'),  # 👈 Nueva URL para eliminar PDFs
    path('search/', views.buscar_contactos, name='buscar_contactos'),
]

# URLs para productos
producto_urlpatterns = [
    path('', views.producto_list, name='producto_list'),
    path('create/', views.producto_create, name='producto_create'),
    path('<int:pk>/', views.producto_detail, name='producto_detail'),
    path('<int:pk>/edit/', views.producto_update, name='producto_update'),
    path('<int:pk>/delete/', views.producto_delete, name='producto_delete'),
]

# URLs para proveedores
proveedor_urlpatterns = [
    path('', views.proveedor_list, name='proveedor_list'),
    path('create/', views.proveedor_create, name='proveedor_create'),
    path('<int:pk>/', views.proveedor_detail, name='proveedor_detail'),
    path('<int:pk>/edit/', views.proveedor_update, name='proveedor_update'),
    path('<int:pk>/delete/', views.proveedor_delete, name='proveedor_delete'),
]

# URLs para precios de proveedores
precio_proveedor_urlpatterns = [
    path('', views.precio_proveedor_list, name='precio_proveedor_list'),
    path('create/', views.precio_proveedor_create, name='precio_proveedor_create'),
    path('<int:pk>/edit/', views.precio_proveedor_update, name='precio_proveedor_update'),
    path('<int:pk>/delete/', views.precio_proveedor_delete, name='precio_proveedor_delete'),
]

# URLs para autenticación
auth_urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/cerrar_sesion.html'), name='logout'),
]

# URLs para Categorías
categoria_urlpatterns = [
    path('', views.categoria_list, name='categoria_list'),
    path('create/', views.categoria_create, name='categoria_create'),
    path('<int:pk>/edit/', views.categoria_update, name='categoria_update'),
    path('<int:pk>/delete/', views.categoria_delete, name='categoria_delete'),
]

# URLs para Subcategorías
subcategoria_urlpatterns = [
    path('', views.subcategoria_list, name='subcategoria_list'),
    path('create/', views.subcategoria_create, name='subcategoria_create'),
    path('<int:pk>/edit/', views.subcategoria_update, name='subcategoria_update'),
    path('<int:pk>/delete/', views.subcategoria_delete, name='subcategoria_delete'),
]

# URLs principales
urlpatterns = [
    path('contacts/', include(contact_urlpatterns)),  # URLs para contactos
    path('products/', include(producto_urlpatterns)),  # URLs para productos
    path('suppliers/', include(proveedor_urlpatterns)),  # URLs para proveedores
    path('suppliers/<int:proveedor_id>/prices/', include(precio_proveedor_urlpatterns)),  # URLs para precios de proveedores
    path('accounts/', include(auth_urlpatterns)),  # URLs para autenticación
    path('search/', buscar_global, name='buscar_global'),  # Búsqueda global
    path('autocompletar/', autocompletar, name='autocompletar'),  # 👈 Nueva URL para autocompletado
    path('upload-csv/', upload_csv, name='upload_csv'),  # Subir archivo CSV
    path('download-csv/', download_csv, name='download_csv'),  # Descargar archivo CSV
    path('categorias/', include(categoria_urlpatterns)),  # URLs para categorías
    path('subcategorias/', include(subcategoria_urlpatterns)),  # URLs para subcategorías
]