from django.db import models
from django.contrib.auth.models import User
from customer_api.models import Customer
from deliver_api.models import Deliver
from decimal import Decimal

COMMISSION_RATE = 0.2  # 20% 外送員抽成

class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    image_url = models.CharField(max_length=200)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.shop_name
    
    

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class OrderStatus(models.IntegerChoices):
    PROVIDER_PREPARING = 0, 'Provider Preparing'
    WAITING_FOR_DELIVERY = 1, 'Waiting for Delivery'
    DELIVERING = 2, 'Delivering'
    COMPLETED = 3, 'Completed'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    deliver = models.ForeignKey(Deliver, on_delete=models.CASCADE, null=True, blank=True, default=None)
    delivery_address = models.CharField(max_length=100)
    total_price = models.PositiveIntegerField()
    delivery_fee = models.PositiveIntegerField()
    provider_fee = models.PositiveIntegerField()
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.PROVIDER_PREPARING)
    created_at = models.DateTimeField(auto_now_add=True)
    memo = models.TextField()

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        self.provider_fee = int(Decimal(self.total_price) * Decimal('0.8'))
        self.delivery_fee = int(Decimal(self.total_price) * Decimal('0.2'))
        super(Order, self).save(*args, **kwargs)
    

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = (('order', 'product'),)

    def __str__(self):
        return f"oid:{self.order_id}-pid{self.product_id}"