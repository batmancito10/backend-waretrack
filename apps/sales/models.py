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

class Factura(BaseModel):
    total = models.FloatField()
    codigo = models.CharField(max_length=20) # generar codigo
    producto = models.ManyToManyField(Producto)
    servicio = models.ManyToManyField(Servicio)
    funcionario = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = ''.join(random.choice('0123456789') for _ in range(12))
        super().save(*args, **kwargs)