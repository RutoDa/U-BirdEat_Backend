from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Provider, Product, Order, OrderDetail
from .serializers import ProviderSerializer, ProfileSerializer, ProductSerializer, OrderSerializer, OrderDetailSerializer, SimpleOrderSerializer
from .permissions import IsProvider



class RegisterView(APIView):
    """
    提供商家註冊 (POST) 的功能
    The API endpoint that allows provider to be registered.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    提供取得商家資訊 (GET) 和更新商家資訊 (PUT) 的功能
    The API endpoint that allows provider to retrieve and update their profile.
    """
    queryset = Provider.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user)
        except Provider.DoesNotExist:
            return None


class ProductsView(generics.ListCreateAPIView):
    """
    提供列出商家有的商品 (GET) 和新增商品 (POST) 的功能
    The API endpoint that allows provider to list and create products.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_queryset(self):
        return Product.objects.filter(provider=self.request.user.provider)
    
    def perform_create(self, serializer):
        serializer.save(provider=self.request.user.provider)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    提供取得單個商品資訊 (GET)、更新商品資訊 (PUT/PATCH) 和刪除商品 (DELETE) 的功能
    The API endpoint that allows provider to retrieve, update and delete products.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_queryset(self):
        return Product.objects.filter(provider=self.request.user.provider)
    

class OrdersView(generics.ListAPIView):
    """
    提供列出商家的訂單 (GET) 的功能
    The API endpoint that allows provider to list orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_queryset(self):
        return Order.objects.filter(provider=self.request.user.provider)



class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    提供取得單個訂單資訊 (GET)、更新訂單資訊 (PUT/PATCH) 和刪除訂單 (DELETE) 的功能
    The API endpoint that allows provider to retrieve, update and delete orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_queryset(self):
        return Order.objects.filter(provider=self.request.user.provider)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=kwargs['pk'])
            order_detail = OrderDetail.objects.filter(order=kwargs['pk'])
            order_serializer = OrderSerializer(order)
            product_serializer = OrderDetailSerializer(order_detail, many=True)
            data = {
            'order_info': order_serializer.data,
            'product_info': product_serializer.data
            }
            return Response(data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class IncomeView(APIView):
    """
    提供取得商家總收入的功能
    The API endpoint that allows provider to retrieve their total income.
    """
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get(self, request):
        orders = Order.objects.filter(provider=request.user.provider, status__gte=1)
        order_serializer = SimpleOrderSerializer(orders, many=True)
        total_income = sum(order.provider_fee for order in orders)
        return Response({'total_income': total_income, 'orders': order_serializer.data})