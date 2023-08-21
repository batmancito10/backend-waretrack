from rest_framework import routers
from .api import ProveedorViewSets, PedidoViewSets

router = routers.DefaultRouter()

router.register('proveedor', ProveedorViewSets, 'proveedor')
router.register('pedido', PedidoViewSets, 'pedido')


urlpatterns = router.urls