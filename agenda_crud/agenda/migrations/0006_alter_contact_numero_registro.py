# Generated by Django 5.1.6 on 2025-02-27 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_alter_contact_options_contact_numero_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='numero_registro',
            field=models.CharField(default='0000-000', max_length=8, unique=True, verbose_name='Número de Registro'),
        ),
    ]
