from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ClienteSerializer, FacturaSerializer
from .permissions import VentasPermission
from .serializers import Through_venta_servicioSerializer, Through_venta_productoSerializer
from ..models import Factura, Through_venta_producto, Through_venta_servicio, Cliente
from apps.catalog.models import Producto, Servicio
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
            instance = list(Factura.objects.filter(sede__company=company.id, deleted_at=None).values())
        else:
            instance = list(Factura.objects.filter(sedes__id__in=sedes_id, deleted_at=None).values())

        for ob in instance:
            ob["servicio"] = (list(Through_venta_servicio.objects.filter(factura=ob["id"], deleted_at=None).values(
                "unidades",
                "servicio_id",
                "created_at",
                "id",
            )))
            ob["producto"] = (list(Through_venta_producto.objects.filter(factura=ob["id"], deleted_at=None).values(
                "unidades",
                "producto_id",
                "created_at",
                "id",
            )))

        return Response(instance, status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def sedes(self, request, *args, **kwargs):
        id_sede = kwargs.get('pk')
        facturas = Factura.objects.filter(sede=id_sede, deleted_at=None)
        facturas = FacturaSerializer(facturas, many=True).data

        for ob_fact in facturas:
            ob_fact["producto"]=list(Through_venta_producto.objects.filter(producto__id__in=ob_fact["producto"], deleted_at=None).values())
            lista = []
            for ob in ob_fact["producto"]:
                producto = Producto.objects.filter(id=ob["producto_id"], deleted_at=None).values().first()
                producto["unidades"] = ob["unidades"]
                lista.append(producto)
            ob_fact["producto"] = lista
            

        for ob_fact in facturas:
            ob_fact["servicio"]=list(Through_venta_servicio.objects.filter(servicio__id__in= ob_fact["servicio"], deleted_at=None).values())
            lista = []
            for ob in ob_fact["servicio"]:
                servicio = Servicio.objects.filter(id=ob["servicio_id"], deleted_at=None).values().first()
                servicio["unidades"] = ob["unidades"]
                lista.append(servicio)
            ob_fact["servicio"] = lista
        
        
        
        return Response(facturas, status.HTTP_200_OK)

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

        cliente, _ = Cliente.objects.get_or_create(cc=cliente , deleted_at=None)

        data = request.data
        data["cliente"] = cliente.id
        data["funcionario"] = request.user.id


        factura = FacturaSerializer(data=data)
        factura.is_valid(raise_exception=True)
        instance_factura = factura.save()

        if not instance_factura.sede.nombre in list(cliente.sede.values_list("nombre", flat=True)):
            cliente.sede.set([instance_factura.sede])

        id_factura = instance_factura.id

        for ob in productos:
            instance = Through_venta_productoSerializer(data={
                "producto":ob["producto"],
                "factura":id_factura,
                "unidades":ob["unidades"],}
            )
            instance.is_valid(raise_exception=True)
            instance_producto = instance.save()
            stock = Through_stock.objects.filter(producto=instance_producto.producto, sede=instance_factura.sede, deleted_at=None).first()
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