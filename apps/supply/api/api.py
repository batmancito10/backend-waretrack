from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_list_or_404
from apps.supply.models import Pedido, through_infoPedido
from .serializers import ProveedorSerializer, PedidoSerializer, through_infoPedidoSerializer, through_infoPedidoTotalSerializer


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
                "producto")
        return Response(instance_pedido,status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = self.get_serializer(instance).data

        instance_tho = through_infoPedido.objects.filter(deleted_at=None, pedido=instance["id"])
        instance["producto"] = through_infoPedidoTotalSerializer(instance_tho, many=True).data

        return Response(instance, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Vista para crear pedidos y productos del pedido


        Para crear el pedido con los productos directamente se tiene que enviar la instancia de pedido_producto
        'producto'=[{'id'=int,'cantidad': int, 'precio_unitario': float, 'producto': int}]
        """
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
    
    @action(detail=False, methods=['post'])#, permission_classes=[PollGroupPermission]
    def producto(self, request):
        """
        vista para agregar productos a un pedido


        Esta vista es para agregar un producto o productos a un pedido
        """
        data = request.data
        if not isinstance(data, list):
            data = [data]
        serializer = through_infoPedidoSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message":"Se ha agregado correctamente"}, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        """
        vista para editar un pedido y sus productos


        Para editar el pedido se hace normal, pero si quieres editar los productos de los pedidos hay que enviar obligatoriamente el 'id' del producto_pedido
        'producto'=[{'id'=1...}]
        """
        
        instance = self.get_object()
        instance = PedidoSerializer(instance, data=request.data, partial=True)
        instance.is_valid(raise_exception=True)
        instancia_pedido = instance.save()

        productos = request.data.get("producto", [])
        for ob in productos:
            try:
                id = ob["id"]
            except KeyError:
                return Response({"message":"Falta el campo 'id' en uno de los productos"},status=status.HTTP_402_PAYMENT_REQUIRED)

            instance = get_list_or_404(through_infoPedido, deleted_at=None, id=id, pedido=instancia_pedido.id)[0]
            instance = through_infoPedidoSerializer(instance, data=ob, partial=True)
            instance.is_valid(raise_exception=True)
            instance.save()

        return Response({"message":"El producto se actualizó correctamente"},status=status.HTTP_200_OK)