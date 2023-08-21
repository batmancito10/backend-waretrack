from rest_framework import viewsets
from .serializers import ProveedorSerializer, PedidoSerializer


class ProveedorViewSets(viewsets.ModelViewSet):
    queryset = ProveedorSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ProveedorSerializer

class PedidoViewSets(viewsets.ModelViewSet):
    queryset = PedidoSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = PedidoSerializer
