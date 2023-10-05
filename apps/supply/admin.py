from django.contrib import admin
from apps.supply.models import Proveedor, Pedido,through_infoPedido


# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Pedido)
admin.site.register(through_infoPedido)