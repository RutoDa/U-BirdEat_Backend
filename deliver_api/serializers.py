from rest_framework import generics, permissions, status
from rest_framework import serializers
from .models import Deliver
from customer_api.models import Customer
from provider_api.models import Order, Provider
from django.contrib.auth.models import User


class DeliverSerializer(serializers.Serializer):
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

        deliver = Deliver.objects.create(
            user=user,
            real_name=validated_data['real_name'],
            phone=validated_data['phone']
        )
        return deliver
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliver
        fields = ['real_name', 'phone']
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'delivery_fee', 'status', 'created_at']
        read_only_fields = ['id', 'delivery_fee', 'created_at']
    

class CustomerSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['real_name', 'phone']    


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['shop_name', 'address']


class OrderDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.IntegerField()
    customer = CustomerSerilizer()
    provider = ProviderSerializer()
    total_price = serializers.IntegerField()
    delivery_fee = serializers.IntegerField()
    delivery_address = serializers.CharField(max_length=100)
    
class SimpleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'delivery_fee', 'created_at']