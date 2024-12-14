from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Customer
from provider_api.models import Order, OrderStatus, Provider, Product, OrderDetail
from .serializers import CustomerSerializer, ProfileSerializer, ProviderSerializer, ProductSerializer, OrderSerializer, OrderProductSerializer, OrderInfoSerializer
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
    

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    提供取得顧客資訊 (GET) 和更新顧客資訊 (PUT) 的功能
    """
    queryset = Customer.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user)
        except Customer.DoesNotExist:
            return None


class ProvidersView(generics.ListAPIView):
    """
    提供列出所有商家 (GET) 的功能
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]


class ProivderDetailView(APIView):
    """
    提供取得單個商家資訊 (GET) 的功能
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get(self, request, pk):
        try:
            provider = Provider.objects.get(id=pk)
            products = provider.product_set.all()
            provider_serializer = ProviderSerializer(provider)
            products_serializer = ProductSerializer(products, many=True)
            return Response({'provider': provider_serializer.data, 'products': products_serializer.data})
        except Provider.DoesNotExist:
            raise NotFound()


class OrderView(APIView):
    """
    提供下訂單 (POST) 的功能
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def post(self, request):
        order_data = request.data.get('order_detail')
        products_data = request.data.get('products')
        
        order_serializer = OrderSerializer(data=order_data)
        if not order_serializer.is_valid():
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        products_serializer = OrderProductSerializer(data=products_data, many=True)
        if not products_serializer.is_valid():
            return Response(products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            provider = Provider.objects.get(id=order_serializer.validated_data['provider'])
        except Provider.DoesNotExist:
            return Response({'error': '無效的供應商'}, status=status.HTTP_404_NOT_FOUND)

        order = Order.objects.create(
            customer=request.user.customer,
            provider=provider,
            delivery_address=order_serializer.validated_data['delivery_address'],
            memo=order_serializer.validated_data['memo'],
            total_price=0,
            status=OrderStatus.PROVIDER_PREPARING
        )

        products = []
        total_price = 0
        for product_data in products_serializer.validated_data:
            try:
                product = provider.product_set.get(id=product_data['id'])
            except Product.DoesNotExist:
                return Response({'error': '無效的商品'}, status=status.HTTP_404_NOT_FOUND)
            count = product_data['count']
            if count == 0:
                continue
            elif count < 0:
                return Response({'error': '數量必須是正整數'}, status=status.HTTP_400_BAD_REQUEST)
            OrderDetail.objects.create(
                order=order,
                product=product,
                count=count
            )
            products.append({
                'name': product.name,
                'price': product.price,
                'count': count
            })
            total_price += product.price * product_data['count']
        order.total_price = total_price
        order.save()
        order_data = {
            "id": order.id,
            "shop_name": order.provider.shop_name,
            "deliver_name": None,
            "status": order.status,
            "total_price": order.total_price,
            "created_at": order.created_at,
            "memo": order.memo,
            'products': products
        }
        order_data_serializer = OrderInfoSerializer(data=order_data)
        if order_data_serializer.is_valid():
            return Response(order_data_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_data_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(APIView):
    """
    提供取得單個訂單資訊 (GET) 的功能
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get(self, request, pk):
        try:
            order =  Order.objects.get(id=pk, customer=request.user.customer)
            order_details = order.orderdetail_set.all()
            products = [{"name": detail.product.name, 
                         "price": detail.product.price,
                         "count": detail.count} for detail in order_details]            
            order_data = {
                "id": order.id,
                "shop_name": order.provider.shop_name,
                "deliver_name": order.deliver.real_name if order.deliver else None,
                "status": order.status,
                "total_price": order.total_price,
                "created_at": order.created_at,
                "memo": order.memo,
                'products': products
            }
            order_data_serializer = OrderInfoSerializer(data=order_data)
            if order_data_serializer.is_valid():
                return Response(order_data_serializer.data)
            return Response(order_data_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Order.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


# TODO: ChatRobotView

# TODO: RandomChoiceView