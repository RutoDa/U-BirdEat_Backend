from django.contrib import admin
from .models import Provider, Product, Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1
    readonly_fields = ('product', 'count')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'provider', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'provider__shop_name')
    inlines = [OrderDetailInline]

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'count')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'provider', 'price', 'created_at')
    list_filter = ('provider', 'created_at')
    search_fields = ('name', 'provider__shop_name')

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'address', 'category', 'image_url')
    search_fields = ('shop_name', 'category')