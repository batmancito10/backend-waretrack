# Generated by Django 4.2.4 on 2023-09-19 03:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("supply", "0003_pedido_created_at_pedido_deleted_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="proveedor",
            name="imagen",
            field=models.ImageField(null=True, upload_to=""),
        ),
    ]