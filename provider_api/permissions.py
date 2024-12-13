from django.utils import timezone
from rest_framework.permissions import BasePermission

from provider_api.models import Provider

class IsProvider(BasePermission):
    message = "只有商家才能使用"
    def has_permission(self, request, view):
        try:
            provider = Provider.objects.get(user=request.user)
        except Provider.DoesNotExist:
            return False
        return True
