import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Filtro para obtener el nombre del archivo sin la ruta."""
    return os.path.basename(value)