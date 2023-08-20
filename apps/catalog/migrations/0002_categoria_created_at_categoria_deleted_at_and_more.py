# Generated by Django 4.2.4 on 2023-08-19 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="categoria",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Fecha de creación"
            ),
        ),
        migrations.AddField(
            model_name="categoria",
            name="deleted_at",
            field=models.DateTimeField(
                blank=True, default=None, null=True, verbose_name="Fecha de eliminación"
            ),
        ),
        migrations.AddField(
            model_name="producto",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Fecha de creación"
            ),
        ),
        migrations.AddField(
            model_name="producto",
            name="deleted_at",
            field=models.DateTimeField(
                blank=True, default=None, null=True, verbose_name="Fecha de eliminación"
            ),
        ),
        migrations.AddField(
            model_name="servicio",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Fecha de creación"
            ),
        ),
        migrations.AddField(
            model_name="servicio",
            name="deleted_at",
            field=models.DateTimeField(
                blank=True, default=None, null=True, verbose_name="Fecha de eliminación"
            ),
        ),
        migrations.AddField(
            model_name="through_stock",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="Fecha de creación"
            ),
        ),
        migrations.AddField(
            model_name="through_stock",
            name="deleted_at",
            field=models.DateTimeField(
                blank=True, default=None, null=True, verbose_name="Fecha de eliminación"
            ),
        ),
    ]