from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from apps.base.api.serializers import GroupSerializer
from apps.user.models import Funcionario
from apps.company.api.serializers import SedeSerializer



class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        exclude = ("user_permissions","date_joined","is_active","is_staff","is_superuser","username")
        read_only_fields = ("last_login","created_at")

    def validate(self, data):
        if 'sede' not in data or not data["sede"]:
            raise serializers.ValidationError({"sede": '"sede" es un campo requerido'})

        return data
    # def validate_sede(self, value):
    #     if not value:
    #         raise serializers.ValidationError('"sede" es un campo requerido')
    #     return value
    

    def create(self, validated_data):
        email = validated_data['email']
        if self.Meta.model.objects.filter(email=email).exists():
            raise ValidationError({'message': 'El usuario ya está registrado.'}, code=status.HTTP_409_CONFLICT)

        username = validated_data.get('username', email)
        password = validated_data['password']
        validated_data['username'] = username
        validated_data['password'] = make_password(password)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data['password']
            validated_data['password'] = make_password(password)
        if 'email' in validated_data:
            validated_data['username'] = validated_data['email']

        return super().update(instance, validated_data)

    def partial_update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data['password']
            validated_data['password'] = make_password(password)
        if 'email' in validated_data:
            validated_data['username'] = validated_data['email']

        return super().partial_update(instance, validated_data)
    
class FuncionarioTotalSerialiser(serializers.ModelSerializer):
    sede = SedeSerializer(many=True)
    groups = GroupSerializer(many=True)
    class Meta:
        model = Funcionario
        exclude = ("user_permissions","date_joined","is_staff","is_superuser","username", "password")