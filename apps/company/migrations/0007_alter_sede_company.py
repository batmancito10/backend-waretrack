# Generated by Django 4.2.4 on 2023-10-05 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0006_rename_logo_company_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sede",
            name="company",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="company.company",
            ),
        ),
    ]