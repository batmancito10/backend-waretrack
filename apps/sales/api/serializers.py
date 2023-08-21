from rest_framework import serializers
from apps.sales.models import Cliente, Factura


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
