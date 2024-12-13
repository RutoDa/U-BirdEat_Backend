from rest_framework import serializers
from .models import Provider, Product, Order, OrderDetail
from django.contrib.auth.models import User


class ProviderSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)
    shop_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=100)
    image_url = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=50)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("密碼不一致")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        provider = Provider.objects.create(
            user=user,
            shop_name=validated_data['shop_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            image_url=validated_data['image_url'],
            category=validated_data['category']
        )
        return provider
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['shop_name', 'phone', 'address', 'image_url', 'category']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'created_at', 'update_at']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'created_at', 'memo']
        read_only_fields = ['id', 'total_price', 'created_at', 'memo']
        

class SimpleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'created_at']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price']


class OrderDetailSerializer(serializers.Serializer):
    product = SimpleProductSerializer()
    count = serializers.IntegerField()