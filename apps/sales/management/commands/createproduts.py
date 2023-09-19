from django.core.management.base import BaseCommand
from apps.catalog.models import Producto
from apps.catalog.api.serializers import ProductoSerializer, CategoriaSerializer
from apps.company.models import Company, Sede
import json

class Command(BaseCommand):
    help = 'Crea los Producto'

    def handle(self, *args, **kwargs):
        index=0
        sedes_instances=Sede.objects.all()[:3]
        with open("apps/sales/jsons/productos.json", "r", encoding="utf-8") as JSONProductos:
            productos = json.load(JSONProductos)
        with open("apps/sales/jsons/categorias.json", "r", encoding="utf-8") as JSONCategorias:
            categorias = json.load(JSONCategorias)
        if not Producto.objects.filter().first():

            id=Company.objects.filter().values("id").first()

            categoria_instance = [{"company": id["id"], **ob} for ob in categorias]
            categoria_instance = CategoriaSerializer(data=categoria_instance, many=True)
            categoria_instance.is_valid(raise_exception=True)
            categoria_instance.save()

            producto_instance = ProductoSerializer(data=productos, many=True)
            producto_instance.is_valid(raise_exception=True)
            producto_instance.save()

        else:
            self.stdout.write(f"{self.style.NOTICE('ya existen productos')} ... {self.style.SUCCESS('OK')}")