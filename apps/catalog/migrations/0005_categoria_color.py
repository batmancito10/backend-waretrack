# Generated by Django 4.2.4 on 2023-08-20 02:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_categoria_company_alter_producto_sedes"),
    ]

    operations = [
        migrations.AddField(
            model_name="categoria",
            name="color",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
