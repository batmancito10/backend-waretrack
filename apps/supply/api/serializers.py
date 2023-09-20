from rest_framework import serializers
from apps.supply.models import Proveedor, Pedido, through_infoPedido
from apps.catalog.api.serializers import ProductoSerializer


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"
        read_only_fields = ("created_at",)

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"
        read_only_fields = ("created_at",)

class through_infoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = through_infoPedido
        fields = "__all__"
        read_only_fields = ("created_at",)

class through_infoPedidoTotalSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    class Meta:
        model = through_infoPedido
        exclude = ("deleted_at",)
        read_only_fields = ("created_at",)
#=============================================================================================================