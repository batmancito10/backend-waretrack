from rest_framework import serializers
# from waretrack.settings.base import AUTH_USER_MODEL
from django.contrib.auth.models import Group
from django.apps import apps


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('company', 'Company')
        exclude = ("deleted_at",)
        read_only_fields = ("created_at",)

class SedeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('company', 'Sede')
        exclude = ("deleted_at",)
        read_only_fields = ("created_at",)

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('user', 'Funcionario')
        exclude = ("user_permissions","date_joined","is_active","is_staff","is_superuser","password","last_login","deleted_at")
        read_only_fields = ("last_login","created_at")



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ("permissions",)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token_google = serializers.CharField(required=True)

    def create(self, validated_data):
        return validated_data