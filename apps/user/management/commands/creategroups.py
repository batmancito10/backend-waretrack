from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.

class Command(BaseCommand):
    help = 'Crea los grupos de permisos: admin, ventas, bodega, talento.'

    def handle(self, *args, **kwargs):
        # Crear los grupos
        groups = ['admin', 'ventas', 'bodega', 'talento']

        for group_name in groups:
            group, _ = Group.objects.get_or_create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f"Grupo '{group_name}' creado correctamente."))