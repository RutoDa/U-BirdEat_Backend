from rest_framework.permissions import BasePermission
from .models import Deliver

class IsDeliver(BasePermission):
    message = "只有外送員才能使用"
    def has_permission(self, request, view):
        try:
            deliver = Deliver.objects.get(user=request.user)
        except Deliver.DoesNotExist:
            return False
        return True
