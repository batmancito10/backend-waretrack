from rest_framework import routers
from .api import FuncionarioViewsets

router = routers.DefaultRouter()

router.register('funcionario', FuncionarioViewsets, 'funcionario')


urlpatterns = router.urls