from django.contrib import admin
from .models import Provider, Product, Order, OrderDetail


admin.site.register(Provider)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
