from rest_framework import serializers
from .models import Customer
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