from django.db import models
from apps.company.models import Sede
from waretrack.settings.base import AUTH_USER_MODEL
from apps.catalog.models import Producto
from apps.base.models import BaseModel
# Create your models here.

def upload_to_proveedor(instance, filename):
    return f"company {instance.sede.first().company.id}/proveedor/{filename}"

class Proveedor(BaseModel):
    imagen = models.ImageField(upload_to=upload_to_proveedor, null=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    sede = models.ManyToManyField(Sede)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

class Pedido(BaseModel):
    fecha_realizado = models.DateTimeField(null=True, blank=True)
    fecha_llegada = models.DateTimeField(null=True, blank=True)
    estado = models.BooleanField(default=False)
    total = models.FloatField('Total de el pedido')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True)
    funcionario = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    producto = models.ManyToManyField(Producto, through='through_infoPedido')
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.fecha_realizado)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

# Requiere una ManyToMany manual
class through_infoPedido(BaseModel):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()

    def __str__(self):
        return f"{self.producto}"

    class Meta:
        ordering = ["id"]
        verbose_name = 'Producto pedido'
        verbose_name_plural = 'Productos pedidos'