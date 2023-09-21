from django.db import models
from apps.company.models import Sede
from waretrack.settings.base import AUTH_USER_MODEL
from apps.catalog.models import Producto
from apps.base.models import BaseModel
# Create your models here.

class Proveedor(BaseModel):
    imagen = models.ImageField(upload_to="", null=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    sede = models.ManyToManyField(Sede)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

class Pedido(BaseModel):
    fecha_realizado = models.DateTimeField(null=True, blank=True)
    fecha_llegada = models.DateTimeField(null=True, blank=True)
    estado = models.BooleanField(default=False)
    total = models.FloatField('Total de el pedido')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    funcionario = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    producto = models.ManyToManyField(Producto, through='through_infoPedido')
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

# Requiere una ManyToMany manual
class through_infoPedido(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()

    class Meta:
        ordering = ["id"]
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'