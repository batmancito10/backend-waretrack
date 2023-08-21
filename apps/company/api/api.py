from rest_framework import viewsets
from .serializers import CompanySerializer, SedeSerializer


class CompanyViewsets(viewsets.ModelViewSet):
    queryset = CompanySerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = CompanySerializer

class SedeViewsets(viewsets.ModelViewSet):
    queryset = SedeSerializer.Meta.model.objects.filter(deleted_at=None)
    serializer_class = SedeSerializer