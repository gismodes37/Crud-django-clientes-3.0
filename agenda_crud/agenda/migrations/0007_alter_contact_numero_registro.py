# Generated by Django 5.1.6 on 2025-02-27 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0006_alter_contact_numero_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='numero_registro',
            field=models.CharField(default='0000-000', max_length=8, verbose_name='Número de Registro'),
        ),
    ]
