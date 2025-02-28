# Generated by Django 5.1.6 on 2025-02-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0017_remove_contact_observaciones_contact_rut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='rut',
        ),
        migrations.AddField(
            model_name='contact',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='apellidos',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='nombres',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='razon_social',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
