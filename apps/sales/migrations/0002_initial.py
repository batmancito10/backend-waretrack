# Generated by Django 4.2.4 on 2023-11-09 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0001_initial'),
        ('catalog', '0001_initial'),
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='funcionario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='factura',
            name='producto',
            field=models.ManyToManyField(through='sales.Through_venta_producto', to='catalog.producto'),
        ),
        migrations.AddField(
            model_name='factura',
            name='sede',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.sede'),
        ),
        migrations.AddField(
            model_name='factura',
            name='servicio',
            field=models.ManyToManyField(through='sales.Through_venta_servicio', to='catalog.servicio'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='sede',
            field=models.ManyToManyField(to='company.sede'),
        ),
    ]
