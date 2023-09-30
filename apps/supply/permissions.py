from rest_framework.permissions import BasePermission
from apps.base.api.permissions import SAFE_METHODS



class BodegaPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            grupos = list(request.user.groups.values_list('name', flat=True))
            if 'admin' in grupos or 'bodega' in grupos or view.action in SAFE_METHODS:
                return True
        return False