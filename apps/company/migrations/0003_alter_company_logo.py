# Generated by Django 4.2.4 on 2023-08-20 02:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0002_sede_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="Logo",
            field=models.ImageField(
                null=True, upload_to="media/", verbose_name="Logo de la compañia"
            ),
        ),
    ]