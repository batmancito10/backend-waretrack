from rest_framework.routers import DefaultRouter
from .api import ClienteViewSets,FacturaViewSets


router = DefaultRouter()

router.register('cliente',ClienteViewSets, 'cliente')
router.register('factura',FacturaViewSets, 'factura')


urlpatterns = router.urls