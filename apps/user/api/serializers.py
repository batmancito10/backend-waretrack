from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from apps.user.models import Funcionario



class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ("first_name","last_name","email","password","is_active","salario","cargo","groups","sede","deleted_at")
        read_only_fields = ("create_at",)

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