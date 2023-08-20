from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CategoriaSerializer, ServicioSerializer, ProductoSerializer, productoSedeSerializer, Through_stockSerializer
# from apps.catalog.models import 

class CategoriaViewsets(viewsets.ModelViewSet):
    queryset = CategoriaSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

class ServicioViewsets(viewsets.ModelViewSet):
    queryset = ServicioSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ServicioSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

class ProductoViewsets(viewsets.ModelViewSet):
    queryset = ProductoSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

class ProductoSedeListCreate(ListCreateAPIView):
    queryset = productoSedeSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = productoSedeSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Listar productos con su stock y sede


        Esta vista trae todos tus productos con la informacion de el stock en cada una de sus sedes
        """
        productos = self.get_queryset()
        productos = self.get_serializer(productos, many=True).data

        for ob in productos:
            instance = Through_stockSerializer.Meta.model.objects.filter(deleted_at=None, producto=ob["id"])
            ob["sedes"] = Through_stockSerializer(instance, many=True).data


        return Response(productos,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Crear un producto con sede, y stock


        En esta vista puedes crear un producto y asignarle un stock y sede
        """
        stock = request.data.pop("sedes")
        producto = ProductoSerializer(data=request.data)
        producto.is_valid(raise_exception=True)
        producto = producto.save()


        for ob in stock:
            ob["producto"] = producto.id
        tmp = Through_stockSerializer(data=stock, many=True)
        tmp.is_valid(raise_exception=True)
        stock = tmp.save()
        stock = Through_stockSerializer(stock, many=True).data

        respuesta = ProductoSerializer(producto).data
        respuesta["sedes"] = stock
        return Response(respuesta,status=status.HTTP_200_OK)