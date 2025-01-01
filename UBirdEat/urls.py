from django.contrib import admin
from django.urls import include, path
from provider_api import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path("provider/", include("provider_api.urls", namespace='provider_api')),
    path("deliver/", include("deliver_api.urls", namespace='deliver_api')),
    path("customer/", include("customer_api.urls", namespace='customer_api')),
    path("provider-sys/", include("provider_system.urls", namespace='provider_system')),
]
