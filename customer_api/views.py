from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Customer
from provider_api.models import Order, OrderStatus, Provider, Product, OrderDetail
from .serializers import CustomerSerializer, ProfileSerializer, ProviderSerializer, ProductSerializer, OrderSerializer, OrderProductSerializer, OrderInfoSerializer
from .permissions import IsCustomer
from .chatbot import get_chatbot_response
from django.db import models


class RegisterView(APIView):
    """
    提供顧客註冊 (POST) 的功能
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
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
    可透過 ?search=關鍵字 來搜尋商家名稱或類別
    """
    serializer_class = ProviderSerializer 
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        queryset = Provider.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(shop_name__icontains=search) | 
                models.Q(category__icontains=search) 
            )
        return queryset


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


class OrdersView(APIView):
    """
    提供列出所有訂單 (GET) 的功能
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def get(self, request):
        orders = request.user.customer.order_set.all().order_by('-created_at')
        order_data = []
        for order in orders:
            order_data.append({
                "id": order.id,
                "shop_name": order.provider.shop_name,
                "deliver_name": order.deliver.real_name if order.deliver else None,
                "status": order.status,
                "total_price": order.total_price,
                "created_at": order.created_at,
            })
        return Response(order_data)


class OrderView(APIView):
    """
    提供下訂單 (POST) 的功能
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def post(self, request):
        order_data = request.data.get('order_detail')
        products_data = request.data.get('products')
        
        # Set default memo if empty
        if not order_data.get('memo'):
            order_data['memo'] = '無備註'
        
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


class ChatRobotView(APIView):
    """
    智能機器人功能（機器人可以透過聊天了解顧客需求，並推薦餐廳與商品）
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def post(self, request):
        prompt = request.data.get('prompt')
        if prompt is None:
            return Response({'error': '請提供對話內容'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = get_chatbot_response(request.user.customer, prompt)
            return Response({'response': response})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        records = request.user.customer.chatrecord_set.all().order_by('created_at')
        history = list()
        for record in records:
            history.append({
                'role': record.role,
                'content': record.content,
                'created_at': record.created_at
            })
        return Response({'history': history})
    
    def delete(self, request):
        request.user.customer.chatrecord_set.all().delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class RandomChoiceView(APIView):
    """
    提供隨機選餐功能（若顧客不知道要吃什麼，只要給定預算，可以透過此功能讓系統幫你搭配並下定單）
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def post(self, request):
        budget = request.data.get('budget')
        delivery_address = request.data.get('delivery_address')
        
        if budget is None:
            return Response({'error': '請提供預算'}, status=status.HTTP_400_BAD_REQUEST)
        if delivery_address is None:
            return Response({'error': '請提供送餐地址'}, status=status.HTTP_400_BAD_REQUEST)
        
        max_retries = Provider.objects.count()
        retries = 0
        while retries < max_retries:
            provider = Provider.objects.order_by('?').first()
            if provider is None:
                retries += 1
                continue
            remaining_products = provider.product_set.filter(price__lte=budget)
            if remaining_products.exists():
                break
            retries += 1
        else:
            return Response({'error': '無法找到符合預算的供應商'}, status=status.HTTP_404_NOT_FOUND)
           
        
        order = Order.objects.create(
            customer=request.user.customer,
            provider=provider,
            delivery_address=delivery_address,
            memo='隨機選餐',
            total_price=0,
            status=OrderStatus.PROVIDER_PREPARING
        )
        
        
        products_selected = dict()
        total_price = 0

        while budget > 0:
            remaining_products = provider.product_set.filter(price__lte=budget)
            if not remaining_products.exists:
                break
            
            # 隨機選擇一個商品
            product = remaining_products.order_by('?').first()
            if product is None:
                break
            
            if product.id in products_selected:
                order_detail_item = OrderDetail.objects.get(order=order, product=product)
                order_detail_item.count += 1
                order_detail_item.save()            
                products_selected[product.id]['count'] += 1
            else:
                OrderDetail.objects.create(
                    order=order,
                    product=product,
                    count=1
                )
                products_selected[product.id] = {
                    'name': product.name,
                    'price': product.price,
                    'count': 1
                }
            total_price += product.price
            budget -= product.price

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
            'products': list(products_selected.values())
        }
        order_data_serializer = OrderInfoSerializer(data=order_data)
        if order_data_serializer.is_valid():
            return Response(order_data_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_data_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)