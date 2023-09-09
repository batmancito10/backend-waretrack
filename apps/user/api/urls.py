from rest_framework import routers
from .api import FuncionarioViewsets, GruposList

router = routers.DefaultRouter()

router.register('funcionario', FuncionarioViewsets, 'funcionario')
router.register('groups', GruposList, 'groups')


urlpatterns = router.urls