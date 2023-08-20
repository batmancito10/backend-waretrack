from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CompanySerializer, SedeSerializer


class CompanyViewsets(viewsets.ModelViewSet):
    queryset = CompanySerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

class SedeViewsets(viewsets.ModelViewSet):
    queryset = SedeSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = SedeSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]