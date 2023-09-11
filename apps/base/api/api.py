
from rest_framework import permissions, status, viewsets
from drf_yasg.views import get_schema_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.apps import apps
from .serializers import GroupSerializer
from drf_yasg import openapi
from .serializers import UserDetailsSerializer,CompanyDetailsSerializer,SedeDetailsSerializer,EmailSerializer


schema_view = get_schema_view(
    openapi.Info(
        title="APIWaretrack",
        default_version="v1",
        description="Documentacion completa de API Waretrack",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="moren1viguel@gmail.com"),
        license=openapi.License(name="licencia para uso exclusivo de Waretrack"),
        schemes=['http', 'https'],
    ),
        public=True,
        permission_classes=[permissions.AllowAny],
)

from rest_framework.views import APIView
from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.api.serializers import FuncionarioTotalSerialiser



def loginTokenUser(request, userr):
    if not userr.is_active:
        return Response({"detail": "Usuario inactivo"},status=status.HTTP_401_UNAUTHORIZED)
    login(request, userr)

    refresh = RefreshToken.for_user(userr)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    tokens = {"access":access_token, "refresh":refresh_token}
    tokens["user"] = FuncionarioTotalSerialiser(userr).data
    return tokens


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Login y sistema de tokens JWT


        Esta vista construye un token JWT para autentificacion en toda la API y un tokent refresh para refrescar el JWT
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not user.is_active:
            return Response({"detail": "Usuario inactivo"},status=status.HTTP_401_UNAUTHORIZED)

        # Iniciar sesión en Django
        login(request, user)


        # Obtener el token JWT
        tokens = serializer.validated_data
        tokens["user"] = UserDetailsSerializer(user).data
        tokens["user"]["company"] = CompanyDetailsSerializer(user.sede.first().company).data
        tokens["user"]["sede"] = SedeDetailsSerializer(user.sede, many=True).data
        tokens["user"]["groups"] = GroupSerializer(user.groups, many=True).data

        return Response(tokens,  status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        """
        Cierre de sesión y eliminación del token JWT

        Esta vista permite cerrar la sesion en la API
        """
        logout(request)
        return Response({"detail": "Sesión finalizada"}, status=status.HTTP_200_OK)

class UserValidationGoogle(viewsets.GenericViewSet):
    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny,]
    # authentication_classes = []
    # @swagger_auto_schema(request_body=EmailSerializer)
    def create(self, request, *args, **kwargs):
        """
        JWT para usuarios de 'Google'
        

        En esta vista se debe pasar el Email de el usuario y el token generado por la API de google
        """
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        Funcionario = apps.get_model('user', 'Funcionario')
        userr =  get_object_or_404(Funcionario, email=email)

        print(userr)

        tokens = loginTokenUser(request, userr)

        return Response(tokens, status=status.HTTP_200_OK)  