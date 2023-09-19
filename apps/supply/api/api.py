from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import F
from apps.supply.models import Pedido, through_infoPedido
from .serializers import ProveedorSerializer, PedidoSerializer, through_infoPedidoSerializer


class ProveedorViewSets(viewsets.ModelViewSet):
    queryset = ProveedorSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ProveedorSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     user = request.user
    #     sede = user.sede.first()



        # instance = self.get_object()
        # instance = ProveedorSerializer(instance)
        # return Response(status=status.HTTP_200_OK)

class PedidoViewSets(viewsets.ModelViewSet):
    queryset = PedidoSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = PedidoSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        sede = user.sede.first()

        instance_pedido = Pedido.objects.filter(deleted_at=None)
        instance_pedido = PedidoSerializer(instance_pedido, many=True).data
        for ob in instance_pedido:
            ob["producto"] = through_infoPedido.objects.filter(deleted_at=None, pedido=ob["id"]).values(
                "id",
                "created_at",
                "cantidad",
                "precio_unitario",
                "producto",
                "pedido")
        return Response(instance_pedido,status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        data_pedido = request.data
        data_pedido["funcionario"] = user.id
        instance = PedidoSerializer(data=data_pedido)
        instance.is_valid(raise_exception=True)
        instance_pedido=instance.save()

        productos = request.data.get("producto", [])
        productos = [{"pedido": instance_pedido.id, **producto} for producto in productos]
        productos = through_infoPedidoSerializer(data=productos, many=True)
        productos.is_valid(raise_exception=True)
        productos.save()

        return Response({"message":"Se registró pedido exitosamente"},status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        instance = PedidoSerializer(instance, data=request.data)
        instance.is_valid(raise_exception=True)
        instance.save()

        return Response({"message":"El producto se actualizó correctamente"},status=status.HTTP_200_OK)