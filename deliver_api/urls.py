from django.urls import path, include
from .views import RegisterView, ProfileView, OrdersView, OrderDetailView, IncomeView

app_name = 'provider_api'

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('income/', IncomeView.as_view(), name='income'),
]
