from django.db import models
from django.utils import timezone

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(null=True, auto_now_add=True,verbose_name='Fecha de creación', blank=True)
    deleted_at = models.DateTimeField(null=True, default=None,verbose_name='Fecha de eliminación', blank=True)

    class Meta:
        abstract = True
    
    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()