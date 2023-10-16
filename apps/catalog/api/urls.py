from rest_framework import routers
from django.urls import path
from .api import CategoriaViewsets, ServicioViewsets, ProductoViewsets, ProductoSedeListCreate,StockUpdateView
router = routers.DefaultRouter()

router.register('categoria', CategoriaViewsets, 'categoria')
router.register('servicio', ServicioViewsets, 'servicio')
router.register('producto', ProductoViewsets, 'producto')

urlpatterns = [
    path('producto/stock/',ProductoSedeListCreate.as_view(),name='producto-stock'),
    path('producto/stock/<int:sede>/<int:producto>/', StockUpdateView.as_view(), name='stock-update'),
]

urlpatterns += router.urls