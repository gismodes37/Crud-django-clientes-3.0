from django.core.management.base import BaseCommand
from agenda.models import Contact
import random

class Command(BaseCommand):
    help = 'Asigna números de registro únicos a contactos existentes'

    def handle(self, *args, **kwargs):
        contacts = Contact.objects.all()
        for contact in contacts:
            # Genera un número de registro único de 8 dígitos
            while True:
                numero_registro = f"{random.randint(10000000, 99999999)}"
                if not Contact.objects.filter(numero_registro=numero_registro).exists():
                    contact.numero_registro = numero_registro
                    contact.save()
                    break
        self.stdout.write(self.style.SUCCESS('Números de registro asignados correctamente.'))