# Generated by Django 5.1.6 on 2025-03-04 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0022_contact_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='rut',
            field=models.CharField(blank=True, help_text='Formato: 00.000.000-0', max_length=12, null=True, verbose_name='Número de Rut'),
        ),
    ]
