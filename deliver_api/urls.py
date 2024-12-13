from django.urls import path, include
from .views import RegisterView, ProfileView

app_name = 'provider_api'

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
