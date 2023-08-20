
from rest_framework import permissions, status
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        # groups = list(user.groups.values_list('name', flat=True))
        # empresa = user.id_domain.first().id_company
        # dominio=user.id_domain.first()
        # if user.id_domain.exists():
            # tokens['domain'] = {"id":dominio.id,"name":dominio.name}
            # tokens['company'] = {"id":empresa.id,"name":empresa.name}
        # else: 
            # tokens['domain'] = None
            # tokens['company'] = None
        # tokens['rol'] = groups
        # tokens['nombre'] = f'{user.first_name} {user.last_name}'

        return Response(tokens,  status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        """
        Cierre de sesión y eliminación del token JWT

        Esta vista permite cerrar la sesion en la API
        """
        logout(request)
        return Response({"detail": "Sesión finalizada"}, status=status.HTTP_200_OK)

