# Generated by Django 5.1.6 on 2025-02-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0016_alter_contact_options_contact_numero_registro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='observaciones',
        ),
        migrations.AddField(
            model_name='contact',
            name='rut',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
