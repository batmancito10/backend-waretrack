# Generated by Django 4.2.4 on 2023-09-21 05:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0012_producto_marca"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="categoria",
            options={
                "ordering": ["id"],
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
            },
        ),
        migrations.AlterModelOptions(
            name="producto",
            options={
                "ordering": ["id"],
                "verbose_name": "Producto",
                "verbose_name_plural": "Productos",
            },
        ),
        migrations.AlterModelOptions(
            name="servicio",
            options={
                "ordering": ["id"],
                "verbose_name": "Servicio",
                "verbose_name_plural": "Servicios",
            },
        ),
        migrations.AlterModelOptions(
            name="through_stock",
            options={
                "ordering": ["id"],
                "verbose_name": "Existencia",
                "verbose_name_plural": "Existencias",
            },
        ),
    ]