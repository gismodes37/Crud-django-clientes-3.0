
---

# Agenda CRUD

## Descripción
Este proyecto es una aplicación web de gestión de contactos, proveedores, productos, categorías y subcategorías. Está desarrollado con Django y proporciona funcionalidades básicas de CRUD (Crear, Leer, Actualizar, Eliminar) para cada entidad.

## Funcionalidades
- **Contactos**: Gestión de contactos con campos como nombre, apellido, teléfono, correo electrónico, etc.
- **Proveedores**: Gestión de proveedores con campos como nombre, contacto, teléfono, email, dirección, etc.
- **Productos**: Gestión de productos con campos como código, nombre, stock, precio neto, margen de venta, flete, subcategoría, etc.
- **Categorías**: Gestión de categorías con campos como código, nombre y descripción.
- **Subcategorías**: Gestión de subcategorías con campos como código, nombre, descripción y una relación con categorías.

## Requisitos
- Python 3.13.2
- Django 5.1.6
- MySQL (o cualquier otro motor de base de datos compatible con Django)

## Instalación
1. **Clona el Repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/agenda_crud.git
   cd agenda_crud
   ```

2. **Crea un Entorno Virtual**:
   ```bash
   python -m venv env
   source env/Scripts/activate  # En Windows
   source env/bin/activate      # En Linux/Mac
   ```

3. **Instala las Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la Base de Datos**:
   - Asegúrate de tener MySQL instalado y ejecutando.
   - Crea una base de datos llamada `agenda_db`.
   - Edita el archivo `agenda_crud/settings.py` y configura la conexión a la base de datos:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'agenda_db',
             'USER': 'tu_usuario',
             'PASSWORD': 'tu_contraseña',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

5. **Aplica las Migraciones**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crea un Superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecuta el Servidor**:
   ```bash
   python manage.py runserver
   ```

   Abre tu navegador y visita `http://127.0.0.1:8000/` para ver la aplicación en acción.

## Uso
- **Contactos**: Accede a `/contacts/` para ver la lista de contactos, crear nuevos contactos, editar o eliminar contactos existentes.
- **Proveedores**: Accede a `/suppliers/` para gestionar proveedores.
- **Productos**: Accede a `/products/` para gestionar productos.
- **Categorías y Subcategorías**: Accede a `/categorias/` y `/subcategorias/` para gestionar categorías y subcategorías.

## Contribuciones
Si deseas contribuir a este proyecto, sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama para tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y commits (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Crea un Pull Request en GitHub.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

### Notas Adicionales
- **Documentación**: Asegúrate de documentar cualquier cambio significativo en el proyecto.
- **Tests**: Si es posible, incluye tests unitarios para asegurar la calidad del código.

Este `README.md` proporciona una guía completa para que otros desarrolladores puedan entender y contribuir a tu proyecto. Si tienes más detalles específicos o necesitas incluir más información, no dudes en ajustarlo.
