from django.core.management.base import BaseCommand
from apps.company.models import Company, Sede
from apps.user.models import Funcionario
from django.contrib.auth.models import Group

import json


class Command(BaseCommand):
    help = 'Crea la compañia "Waretrack" con algunas Sedes.'

    def handle(self, *args, **kwargs):
        company=Company.objects.get_or_create(name="Waretrack")[0]
        self.stdout.write(self.style.SUCCESS("Compañia 'Waretrack' creada correctamente."))

        sedes = [
            {"direccion":"Calle 10 #86-90","nombre":"Casa de Miguel","ciudad":"Bogotá","company":company},
            {"direccion":"Calle 10 #86-90","nombre":"Casa de Daniel","ciudad":"Bogotá","company":company},
            {"direccion":"Calle 10 #86-90","nombre":"Casa de Sebastian","ciudad":"Fusagasugá","company":company},
        ]
        sedes_instances=[]
        for sede in sedes:
            instances = Sede.objects.get_or_create(**sede)[0]
            sedes_instances.append(instances)
            self.stdout.write(f"Sede {self.style.WARNING(instances.nombre)} creada. ... {self.style.SUCCESS('OK')}")
        with open("apps/user/json/usertest.json", "r", encoding="utf-8") as JSONUsers:
            users = json.load(JSONUsers)
        index=0
        for user in users:
            user, create = Funcionario.objects.get_or_create(**user)
            user.sede.set([sedes_instances[index]])
            self.stdout.write(f"Usuario {self.style.NOTICE(user.email)} creado correctamente. ... {self.style.SUCCESS('OK')}")

            # user_.groups.set([group])
            index+=1

        self.stdout.write(self.style.SUCCESS("Se creo correctamente Waretrack."))
