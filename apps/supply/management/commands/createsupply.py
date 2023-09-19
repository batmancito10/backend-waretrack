from django.core.management.base import BaseCommand
from apps.supply.models import Proveedor
from apps.company.models import Sede
import json

class Command(BaseCommand):
    help = 'Crea los proveedor'

    def handle(self, *args, **kwargs):
        index=0
        sedes_instances=Sede.objects.all()[:3]
        with open("apps/supply/jsons/proveedores.json", "r", encoding="utf-8") as JSONProovedor:
            proveedores = json.load(JSONProovedor)
        if not Proveedor.objects.filter().first():
            for ob in proveedores:
                instance = Proveedor.objects.get_or_create(**ob)[0]
                instance.sede.set([sedes_instances[index]])
                index+=1
                self.stdout.write(f"proveedor {self.style.NOTICE(instance.email)} creado correctamente. ... {self.style.SUCCESS('OK')}")
                if index == 3:
                    index = 0
        else:
            self.stdout.write(f"{self.style.NOTICE('ya existen proveedores')} ... {self.style.SUCCESS('OK')}")