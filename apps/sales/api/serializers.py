from rest_framework import serializers
from apps.sales.models import Cliente, Factura
from ..models import Through_venta_producto, Through_venta_servicio


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        exclude = ("deleted_at",)
        read_only_fields = ("created_at",)

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        exclude = ("deleted_at",)
        read_only_fields = ("created_at",)


class Through_venta_productoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Through_venta_producto
        exclude = ("deleted_at",)
        read_only_fields = ("created_at",)

class Through_venta_servicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Through_venta_servicio
        exclude = ("deleted_at",)
        read_only_fields = ("created_at",)