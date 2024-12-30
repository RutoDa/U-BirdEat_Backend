from rest_framework import serializers
from .models import Customer
from provider_api.models import Provider, Product, Order, OrderDetail
from django.contrib.auth.models import User


class CustomerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)
    real_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("密碼不一致")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        customer = Customer.objects.create(
            user=user,
            real_name=validated_data['real_name'],
            phone=validated_data['phone']
        )
        return customer
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['real_name', 'phone']
        

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'shop_name', 'image_url', 'category']
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']
        

class OrderSerializer(serializers.Serializer):
    provider = serializers.IntegerField()
    delivery_address = serializers.CharField(max_length=100)
    memo = serializers.CharField(max_length=300, allow_blank=True)


class OrderProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField(min_value=0)


class OrderProductDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.IntegerField(min_value=0)
    count = serializers.IntegerField(min_value=0)
    

class OrderInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    shop_name = serializers.CharField(max_length=100)
    deliver_name = serializers.CharField(max_length=100, allow_null=True)
    status = serializers.IntegerField()
    total_price = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    memo = serializers.CharField(max_length=300)
    products = OrderProductDetailSerializer(many=True)
    

    