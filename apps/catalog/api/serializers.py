from rest_framework import serializers
from apps.catalog.models import Categoria, Servicio, Producto, Through_stock

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        read_only_fields = ("create_at",)

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"
        read_only_fields = ("create_at",)

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
        read_only_fields = ("create_at",)


class Through_stockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Through_stock
        fields = "__all__"
        read_only_fields = ("create_at",)

class productoSedeSerializer(serializers.ModelSerializer):
    sedes = Through_stockSerializer(many=True)
    class Meta:
        model = Producto
        fields = "__all__"
        read_only_fields = ("create_at",)