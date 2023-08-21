from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CategoriaSerializer, ServicioSerializer, ProductoSerializer, productoSedeSerializer, Through_stockSerializer
# from apps.catalog.models import 

class CategoriaViewsets(viewsets.ModelViewSet):
    queryset = CategoriaSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = CategoriaSerializer

class ServicioViewsets(viewsets.ModelViewSet):
    queryset = ServicioSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ServicioSerializer

class ProductoViewsets(viewsets.ModelViewSet):
    queryset = ProductoSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ProductoSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Obtener todos los detalles de un producto
        
        
        Esta vista trae ademas de el producto, trae el stock en las distintas sedes, los detalles de la categoria
        """
        instace = self.get_object()
        categoria = instace.categoria
        producto_data = self.get_serializer(instace).data
        sedes_instance = Through_stockSerializer.Meta.model.objects.filter(producto=producto_data["id"], deleted_at=None)
        producto_data["sedes"] = Through_stockSerializer(sedes_instance, many=True).data
        producto_data["categoria"] = CategoriaSerializer(categoria).data
        return Response(producto_data, status=status.HTTP_200_OK)

class ProductoSedeListCreate(ListCreateAPIView):
    queryset = productoSedeSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = productoSedeSerializer

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

class ProductoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = productoSedeSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = productoSedeSerializer
