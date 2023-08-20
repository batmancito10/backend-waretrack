from django.db import models
from apps.company.models import Sede
from apps.base.models import BaseModel

# Create your models here.

class Categoria(BaseModel):
    tipoChoice = (
        ('servicio','servicio'),
        ('producto','producto'),
        ('activo','activo')
    )
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=tipoChoice, default='producto')

class Producto(BaseModel):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.FloatField()
    codigo = models.CharField(max_length=20) # Generador de codigo
    Categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    sede = models.ManyToManyField(Sede, through='through_stock')

# Requiere una ManyToMany manual
class through_stock(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)
    stock = models.CharField(max_length=255)

class Servicio(BaseModel):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.FloatField()
    Categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)