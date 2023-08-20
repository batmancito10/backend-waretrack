from rest_framework import serializers
from apps.company.models import Company, Sede

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("create_at",)

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = "__all__"
        read_only_fields = ("create_at",)
