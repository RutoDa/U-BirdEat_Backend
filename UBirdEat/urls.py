from django.contrib import admin
from django.urls import include, path
from provider_api import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    # path('register/', registration, name='register'), # https://jacychu.medium.com/django-jwt%E9%A9%97%E8%AD%89-%E4%B8%8A-eb18e41d999
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path("provider/", include("provider_api.urls", namespace='provider_api')),
]
