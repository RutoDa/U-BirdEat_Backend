from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Deliver
from provider_api.models import Order, OrderStatus
from .serializers import DeliverSerializer, ProfileSerializer, OrderSerializer, OrderDetailSerializer, SimpleOrderSerializer
from .permissions import IsDeliver


class RegisterView(APIView):
    """
    提供外送員註冊 (POST) 的功能
    The API endpoint that allows deliver to be registered.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = DeliverSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(None, status=status.HTTP_201_CREATED)
            except Exception as e:
                if 'UNIQUE constraint' in str(e):
                    return Response({'error': '帳號已存在'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    提供取得外送員資訊 (GET) 和更新外送員資訊 (PUT) 的功能
    The API endpoint that allows deliver to retrieve and update their profile.
    """
    queryset = Deliver.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeliver]

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user)
        except Deliver.DoesNotExist:
            return None
        

class OrdersView(generics.ListAPIView):
    """
    提供列出外送員可接訂單 (GET) 的功能
    The API endpoint that allows deliver to list orders that can be accepted.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeliver]

    def get_queryset(self):
        return Order.objects.filter(status=OrderStatus.WAITING_FOR_DELIVERY, deliver=None)
    

class OrderDetailView(APIView):
    """
    提供取得單個訂單資訊 (GET) 和接訂單 (PUT) 的功能
    The API endpoint that allows deliver to retrieve and accept an order.
    """
    
    def get(self, request, pk):
        try:
            order =  Order.objects.get(id=pk)
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        try:
            order =  Order.objects.get(id=pk)
            if order.status == OrderStatus.WAITING_FOR_DELIVERY and order.deliver == None:
                order.deliver = request.user.deliver
                order.status = OrderStatus.DELIVERING
                order.save()
            elif order.status == OrderStatus.DELIVERING and order.deliver == request.user.deliver:
                order.status = OrderStatus.COMPLETED
                order.save()
            else:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        

class IncomeView(APIView):
    """
    提供取得外送員總收入的功能
    The API endpoint that allows deliver to retrieve their total income.
    """
    permission_classes = [permissions.IsAuthenticated, IsDeliver]

    def get(self, request):
        orders = Order.objects.filter(deliver=request.user.deliver, status__gte=3).order_by('-created_at')
        order_serializer = SimpleOrderSerializer(orders, many=True)
        total_income = sum(order.delivery_fee for order in orders)
        return Response({'total_income': total_income, 'orders': order_serializer.data})