from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from apps.catalog.permissions import CatalogoPermission
from .serializers import CategoriaSerializer, ServicioSerializer, ProductoSerializer, productoSedeSerializer, Through_stockSerializer
# from apps.catalog.models import 

class CategoriaViewsets(viewsets.ModelViewSet):
    queryset = CategoriaSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = CategoriaSerializer
    permission_classes = [CatalogoPermission]

class ServicioViewsets(viewsets.ModelViewSet):
    queryset = ServicioSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ServicioSerializer
    permission_classes = [CatalogoPermission]

class ProductoViewsets(viewsets.ModelViewSet):
    queryset = ProductoSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = ProductoSerializer
    permission_classes = [CatalogoPermission]

    def list(self, request, *args, **kwargs):
        user = request.user
        grupos = list(user.groups.values_list('name', flat=True))

        if 'admin' in grupos:
            company = user.sede.first().company
            instance_productos = ProductoSerializer.Meta.model.objects.filter(deleted_at=None, sedes__company=company).distinct()
        else:
            sedesArrarId = user.sede.values_list('id', flat=True)
            instance_productos = ProductoSerializer.Meta.model.objects.filter(deleted_at=None, sedes__in=sedesArrarId).distinct()
        instance_productos = ProductoSerializer(instance_productos, many=True).data
        # import pdb; pdb.set_trace()
        return Response(instance_productos, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        producto = ProductoSerializer(data=request.data)
        producto.is_valid(raise_exception=True)
        producto = producto.save()


        tmp = Through_stockSerializer(data={
            "producto":producto.id,
            "sede":request.user.sede.first().id,
            "stock":0,
        })
        tmp.is_valid(raise_exception=True)
        stock = tmp.save()
        # stock = Through_stockSerializer(stock, many=True).data
        return Response({"message":f"Producto agregado a '{request.user.sede.first().nombre}' exitosamente"}, status=status.HTTP_201_CREATED)

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
    permission_classes = [CatalogoPermission]

    def get(self, request, *args, **kwargs):
        """
        Listar productos con su stock y sede


        Esta vista trae todos tus productos con la informacion de el stock en cada una de sus sedes
        """
        user = request.user
        grupos = list(user.groups.values_list('name', flat=True))

        if 'admin' in grupos:
            company = user.sede.first().company
            instance_productos = ProductoSerializer.Meta.model.objects.filter(deleted_at=None, sedes__company=company).distinct()
        else:
            sedesArrarId = user.sede.values_list('id', flat=True)
            instance_productos = ProductoSerializer.Meta.model.objects.filter(deleted_at=None, sedes__in=sedesArrarId).distinct()
        instance_productos = ProductoSerializer(instance_productos, many=True).data
        # productos = self.get_queryset()
        # productos = self.get_serializer(productos, many=True).data

        for ob in instance_productos:
            instance = Through_stockSerializer.Meta.model.objects.filter(deleted_at=None, producto=ob["id"])
            ob["sedes"] = Through_stockSerializer(instance, many=True).data


        return Response(instance_productos,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
    
        """
        Crear un producto con sede, y stock


        En esta vista puedes crear un producto y asignarle un stock y sede
        """
        stock = request.data.pop("sedes",[])
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

class StockUpdateView(UpdateAPIView):
    serializer_class = Through_stockSerializer

    def partial_update(self, request, *args, **kwargs):
        """
        Actualizar el stock de un producto en una sede
        
        
        Se debe de enviar por --URL-- las variables 'sede' y 'producto' y en el BODY el 'stock'
        """
        id_sede = kwargs.get('sede', [])
        id_producto = kwargs.get('producto', [])

        if not id_producto or not id_sede:
            return Response({"message": "faltan parametros para la busqueda"},status.HTTP_402_PAYMENT_REQUIRED)
        try:
            stock =  Through_stockSerializer.Meta.model.objects.filter(sede=id_sede, producto=id_producto).first()
            if not stock:
                return Response({"message": "producto no encontrado"},status.HTTP_404_NOT_FOUND)
            stock.stock = request.data["stock"]
            stock.save()
        except KeyError:
            return Response({"message": "falta el stock para el producto"},status.HTTP_402_PAYMENT_REQUIRED)
            
        return Response(status.HTTP_200_OK)
