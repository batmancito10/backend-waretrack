from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.company.models import Sede
from apps.base.models import BaseModel
# Create your models here.
 

class Funcionario(BaseModel,AbstractUser):
    salario = models.FloatField(null=True)
    cargo = models.CharField(max_length=100, null=True)
    sede = models.ManyToManyField(Sede)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    REQUIRED_FIELDS = ['email','name','last_name','sede',]