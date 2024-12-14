from django.urls import path, include
from .views import RegisterView, ProfileView, ProvidersView, ProivderDetailView, OrderView, OrderDetailView

app_name = 'provider_api'

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('providers/', ProvidersView.as_view(), name='providers'),
    path('providers/<int:pk>/', ProivderDetailView.as_view(), name='provider_detail'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]