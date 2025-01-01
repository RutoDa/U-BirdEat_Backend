from django.urls import path
from .views import *

app_name = 'provider_system'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('product/create/', product_create_view, name='product_create'),
    path('product/edit/<int:product_id>/', product_edit_view, name='product_edit'),
    path('product/delete/<int:product_id>/', product_delete_view, name='product_delete'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('orders/', orders_manage_view, name='orders_manage'),
    path('order/detail/<int:order_id>/', order_detail_view, name='order_detail'),
    path('order/ready/<int:order_id>/', order_ready_view, name='order_ready'),
    path('history/', history_view, name='history'),
    path('income/', income_view, name='income'),
]
