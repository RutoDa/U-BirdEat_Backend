from django.urls import path, include
from .views import RegisterView

app_name = 'provider_api'

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
]
