from rest_framework import routers
from .api import CompanyViewsets, SedeViewsets
router = routers.DefaultRouter()


router.register('company', CompanyViewsets, 'company')
router.register('sede', SedeViewsets, 'sede')

urlpatterns = router.urls