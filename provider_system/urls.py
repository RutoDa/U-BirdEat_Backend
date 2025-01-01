from django.urls import path, include
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
]
