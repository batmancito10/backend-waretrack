# Generated by Django 4.2.4 on 2023-09-21 05:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0004_alter_company_options_alter_sede_options"),
        ("user", "0003_alter_funcionario_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="funcionario",
            options={
                "ordering": ["id"],
                "verbose_name": "Usuario",
                "verbose_name_plural": "Usuarios",
            },
        ),
        migrations.AlterField(
            model_name="funcionario",
            name="cargo",
            field=models.CharField(
                help_text="The position held by the official", max_length=100, null=True
            ),
        ),
        migrations.AlterField(
            model_name="funcionario",
            name="salario",
            field=models.FloatField(help_text="The salary of the official", null=True),
        ),
        migrations.AlterField(
            model_name="funcionario",
            name="sede",
            field=models.ManyToManyField(
                help_text="The headquarters to which an official belongs. A user can belong to several offices.",
                to="company.sede",
            ),
        ),
    ]
