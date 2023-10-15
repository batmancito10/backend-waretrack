from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CompanySerializer, SedeSerializer
from ..models import Sede
from apps.catalog.models import Producto, Through_stock
from apps.catalog.api.serializers import ProductoSerializer
# from apps.catalog.api.serializers import SedeSerializer


class CompanyViewsets(viewsets.ModelViewSet):
    queryset = CompanySerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = CompanySerializer

class SedeViewsets(viewsets.ModelViewSet):
    queryset = SedeSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = SedeSerializer

    @action(detail=True, methods=['get'])
    def stock(self, request, *args, **kwargs):
        """
        Productos y su Stock de una sede
        
        
        Esta vista recive el ID de una sede y retorna los productos que tiene esa sede y cuantos tiene de cada uno   
        """
        id_sede = kwargs.get('pk')
        productos = Producto.objects.filter(sedes=id_sede, deleted_at=None)
        productos = ProductoSerializer(productos, many=True).data
        for producto in productos:
            del producto["sedes"]
            del producto["deleted_at"]
            producto["stock"] = Through_stock.objects.filter(producto=producto["id"], sede=id_sede).values("stock")

        return Response(productos,status.HTTP_200_OK)