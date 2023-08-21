from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProveedorSerializer, PedidoSerializer


class ProveedorViewSets(viewsets.ModelViewSet):
    queryset = ProveedorSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]


class PedidoViewSets(viewsets.ModelViewSet):
    queryset = PedidoSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = PedidoSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
