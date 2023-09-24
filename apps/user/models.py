from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.company.models import Sede
from apps.base.models import BaseModel
# Create your models here.
 
def upload_to_user(instance, filename):
    return f"company {instance.sede.first().company.id}/users/{filename}"

class Funcionario(BaseModel,AbstractUser):
    imagen = models.ImageField(upload_to=upload_to_user, null=True)
    salario = models.FloatField(null=True,help_text=_(
            "The salary of the official"
        ))
    cargo = models.CharField(max_length=100, null=True, help_text=_(
            "The position held by the official"
        ),)
    sede = models.ManyToManyField(Sede, help_text=(
        "The headquarters to which an official belongs. "
        "A user can belong to several offices."
    ))

    class Meta:
        ordering = ["id"]
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    # REQUIRED_FIELDS = ['email','name','last_name','sede',]