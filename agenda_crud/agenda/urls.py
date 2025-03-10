from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    register, custom_login, buscar_global, contact_detail,
    upload_csv, download_csv,
    contact_list, contact_create, contact_update, contact_delete,
    producto_list, producto_create, producto_detail, producto_update, producto_delete,
    proveedor_list, proveedor_create, proveedor_detail, proveedor_update, proveedor_delete,
    precio_proveedor_list, precio_proveedor_create, precio_proveedor_update, precio_proveedor_delete,
    buscar_contactos, autocompletar  # 👈 Agregamos la vista de autocompletado
)

# URLs para contactos
contact_urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='contact_create'),
    path('<int:pk>/edit/', views.contact_update, name='contact_update'),
    path('<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('<int:pk>/', views.contact_detail, name='contact_detail'),
    path('search/', views.buscar_contactos, name='buscar_contactos'),  # Nueva URL para búsqueda de contactos
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
]