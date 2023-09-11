from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .permissions import FuncionarioPermission
from .serializers import FuncionarioSerializer, FuncionarioTotalSerialiser

class FuncionarioViewsets(viewsets.ModelViewSet):
    queryset = FuncionarioSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = FuncionarioSerializer
    permission_classes = [FuncionarioPermission]

    def list(self, request, *args, **kwargs):
        usuario = request.user
        company = usuario.sede.first().company.id
        instance = FuncionarioTotalSerialiser.Meta.model.objects.filter(deleted_at=None, sede__company=company)
        instance = FuncionarioTotalSerialiser(instance,many=True)
        # for ob in instance.data:
        #     print(ob)
        #     ob["groups"] = GroupSerializer(ob.groups, many=True)

        return Response(instance.data, status=status.HTTP_200_OK)

class GruposList(viewsets.GenericViewSet):

    def list(self, reuques, *args, **kwargs):
        instance = list(Group.objects.all().values("id","name"))
        return Response(instance, status=status.HTTP_200_OK)
