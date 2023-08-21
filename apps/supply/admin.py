from django.contrib import admin
from apps.supply.models import Proveedor, Pedido


# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Pedido)