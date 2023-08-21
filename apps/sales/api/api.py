from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import ClienteSerializer, FacturaSerializer


class ClienteViewSets(viewsets.GenericViewSet):
    serializer_class = ClienteSerializer

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

class FacturaViewSets(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer

    def get_queryset(self):
        return FacturaSerializer.Meta.model.objects.filter(deleted_at=None)


    