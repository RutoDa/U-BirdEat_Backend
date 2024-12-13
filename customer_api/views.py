from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Customer
from provider_api.models import Order, OrderStatus
from .serializers import CustomerSerializer
from .permissions import IsCustomer


class RegisterView(APIView):
    """
    提供顧客註冊 (POST) 的功能
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)