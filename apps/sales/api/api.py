from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import ClienteSerializer, FacturaSerializer
from .permissions import VentasPermission
from .serializers import Through_venta_servicioSerializer, Through_venta_productoSerializer
from ..models import Factura, Through_venta_producto, Through_venta_servicio, Cliente
from apps.catalog.models import Through_stock


class ClienteViewSets(viewsets.GenericViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [VentasPermission]

    def get_queryset(self):
        return ClienteSerializer.Meta.model.objects.filter(deleted_at=None)
    
    def list(self, request, *args, **kwargs):
        """
        listar mis clientes
        
        
        Esta vista permite listar los clientes de mi sede o sedes
        """
        instance = self.get_queryset()
        instance = self.get_serializer(instance, many=True).data
        return Response(instance,status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        """
        Crear cliente
        
        
        Esta vista creara o traera clientes
        """
        print(request.data)
        instance = self.get_serializer(data=request.data)
        instance.is_valid(raise_exception=True)
        instance.save()
        return Response(instance.data,status=status.HTTP_201_CREATED)

class FacturaViewSets(viewsets.GenericViewSet):
    serializer_class = FacturaSerializer
    permission_classes = [VentasPermission]

    def get_queryset(self):
        return FacturaSerializer.Meta.model.objects.filter(deleted_at=None)
    
    def list(self, request, *args, **kwargs):
        user = request.user
        company = request.user.sede.first().company
        sedes_id = list(user.sede.values_list("id", flat=True))

        if "admin" in list(request.user.groups.values_list('name', flat=True)):
            instance = list(Factura.objects.filter(sede__company=company.id).values())
        else:
            instance = list(Factura.objects.filter(sedes__id__in=sedes_id).values())

        for ob in instance:
            ob["servicio"] = (list(Through_venta_servicio.objects.filter(factura=ob["id"]).values(
                "unidades",
                "servicio_id",
                "created_at",
                "id",
            )))
            ob["producto"] = (list(Through_venta_producto.objects.filter(factura=ob["id"]).values(
                "unidades",
                "producto_id",
                "created_at",
                "id",
            )))

        return Response(instance, status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        """
        Vista para crear facturas
        
        
        En esta vista se deven enviar los parametros base del modelo, pero en los campos 'servicio' y 'producto' se enviaran los datos de la siguiente forma...
        servicio = [{'servicio'= int, 'unidades'= int}...]
        producto = [{'producto'= int, 'unidades'= int}...]
        """
        servicios = request.data.get('servicio',[])
        productos = request.data.get('producto',[])
        cliente = request.data.get('cc',None)

        cliente, _ = Cliente.objects.get_or_create(cc=cliente)

        data = request.data
        data["cliente"] = cliente.id
        data["funcionario"] = request.user.id

        print(cliente)
        print(data)

        factura = FacturaSerializer(data=data)
        factura.is_valid(raise_exception=True)
        instance_factura = factura.save()
        print(instance_factura.sede, instance_factura.funcionario)

        if not instance_factura.sede.nombre in list(cliente.sede.values_list("nombre", flat=True)):
            cliente.sede.set([instance_factura.sede])
            print(cliente.sede)

        id_factura = instance_factura.id

        for ob in productos:
            instance = Through_venta_productoSerializer(data={
                "producto":ob["producto"],
                "factura":id_factura,
                "unidades":ob["unidades"],}
            )
            instance.is_valid(raise_exception=True)
            instance_producto = instance.save()
            stock = Through_stock.objects.filter(producto=instance_producto.producto, sede=instance_factura.sede).first()
            stock.stock =  stock.stock - instance_producto.unidades
            stock.save()
        for ob in servicios:
            instance = Through_venta_servicioSerializer(data={
                "servicio":ob["servicio"],
                "factura":id_factura,
                "unidades":ob["unidades"],}
            )
            instance.is_valid(raise_exception=True)
            instance.save()

        return Response({"mesagge":"Se ha creado la factura exitosamente"}, status.HTTP_201_CREATED)