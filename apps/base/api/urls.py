from rest_framework import routers
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .api import schema_view, CustomTokenObtainPairView, UserValidationGoogle,Dashboard,CajaVentaGet


router = routers.DefaultRouter()

router.register('token/google', UserValidationGoogle, 'token')
router.register('metricas', Dashboard, 'metricas-default')
router.register('caja', CajaVentaGet, 'caja-view')

urlpatterns = router.urls

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('token/google/', .as_view(), name='validate_user_email_google'),

]