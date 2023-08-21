from django.contrib import admin
from .models import Categoria, Servicio, Producto, Through_stock

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Servicio)
admin.site.register(Producto)
admin.site.register(Through_stock)
