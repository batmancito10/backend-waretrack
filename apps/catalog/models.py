import random
from django.db import models
from apps.company.models import Company, Sede
from apps.base.models import BaseModel

# Create your models here.

class Categoria(BaseModel):
    tipoChoice = (
        ('servicio','servicio'),
        ('producto','producto'),
        ('activo','activo')
    )
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True)
    tipo = models.CharField(max_length=20, choices=tipoChoice, default='producto')
    color = models.CharField(max_length=20, null=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Producto(BaseModel):
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=100, null=True)
    descripcion = models.TextField(null=True)
    precio = models.FloatField()
    codigo = models.CharField(max_length=20, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    sedes = models.ManyToManyField(Sede, through='Through_stock', related_name='productos')

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = ''.join(random.choice('0123456789') for _ in range(12))
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["id"]
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

# Requiere una ManyToMany manual
class Through_stock(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=False)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, blank=False)
    stock = models.IntegerField(default=0)
    
    class Meta:
        ordering = ["id"]
        verbose_name = 'Existencia'
        verbose_name_plural = 'Existencias'

class Servicio(BaseModel):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    sedes = models.ManyToManyField(Sede)
    
    class Meta:
        ordering = ["id"]
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'