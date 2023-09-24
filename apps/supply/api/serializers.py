from rest_framework import serializers
from apps.supply.models import Proveedor, Pedido, through_infoPedido
from apps.catalog.api.serializers import ProductoSerializer
from apps.company.api.serializers import SedeSerializer


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"
        read_only_fields = ("created_at",)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if 'sede' not in data or not data["sede"]:
                raise serializers.ValidationError({"sede": '"sede" es un campo requerido'})
        return data

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

class ProveedorSedeSerializer(serializers.ModelSerializer):
    sede = SedeSerializer(many=True)
    class Meta:
        model = Proveedor
        fields = "__all__"
        read_only_fields = ("created_at",)
#=============================================================================================================