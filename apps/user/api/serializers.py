from rest_framework import serializers
from apps.user.models import Funcionario



class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = "__all__"
        read_only_fields = ("create_at",)