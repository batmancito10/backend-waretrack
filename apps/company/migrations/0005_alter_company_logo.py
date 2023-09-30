# Generated by Django 4.2.4 on 2023-09-24 00:34

import apps.company.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0004_alter_company_options_alter_sede_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="Logo",
            field=models.ImageField(
                null=True,
                upload_to=apps.company.models.upload_to_logo_company,
                verbose_name="Logo de la compañia",
            ),
        ),
    ]