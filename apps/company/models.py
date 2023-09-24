from django.db import models
from apps.base.models import BaseModel
# Create your models here.

def upload_to_logo_company(instance, filname):
    return f"company {instance.id}/logo/{filname}"

class Company(BaseModel):
    name = models.CharField(max_length=100)
    logo = models.ImageField('Logo de la compañia', upload_to=upload_to_logo_company, null=True)
    
    class Meta:
        ordering = ["id"]
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañia'

class Sede(BaseModel):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'