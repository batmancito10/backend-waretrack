# Generated by Django 4.2.4 on 2023-08-20 14:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0010_servicio_sedes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="servicio",
            old_name="Categoria",
            new_name="categoria",
        ),
    ]