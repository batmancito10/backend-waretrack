from django.db import models
import random
from waretrack.settings.base import AUTH_USER_MODEL
from apps.catalog.models import Producto, Servicio
from apps.company.models import Sede
from apps.base.models import BaseModel

# Create your models here.

class Cliente(BaseModel):
    cc = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255, null=True)
    apellido = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    direccion = models.CharField(max_length=255, null=True)
    sede = models.ManyToManyField(Sede)
    
    class Meta:
        ordering = ["id"]
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return f"{self.cc}"

class Factura(BaseModel):
    total = models.FloatField()
    codigo = models.CharField(max_length=20, blank=True) # generar codigo
    producto = models.ManyToManyField(Producto, through='Through_venta_producto')
    servicio = models.ManyToManyField(Servicio, through='Through_venta_servicio')
    funcionario = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = ''.join(random.choice('0123456789') for _ in range(12))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

    def __str__(self):
        return f"{self.codigo}"

# Requiere una ManyToMany manual
class Through_venta_servicio(BaseModel):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True, blank=False)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=False)
    unidades = models.IntegerField(default=1)


class Through_venta_producto(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=False)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=False)
    unidades = models.IntegerField(default=1)