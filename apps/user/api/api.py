from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import FuncionarioSerializer

class FuncionarioViewsets(viewsets.ModelViewSet):
    queryset = FuncionarioSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = FuncionarioSerializer

    # def create(self, )
