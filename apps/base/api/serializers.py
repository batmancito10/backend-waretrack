from rest_framework import serializers
# from waretrack.settings.base import AUTH_USER_MODEL
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