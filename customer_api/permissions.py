from rest_framework.permissions import BasePermission
from .models import Customer


class IsCustomer(BasePermission):
    message = "只有顧客才能使用"
    def has_permission(self, request, view):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return False
        return True
