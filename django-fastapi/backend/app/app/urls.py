from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import jwks_view 

urlpatterns = [
    path('admin/', admin.site.urls),

        # JWT Auth routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('.well-known/jwks.json', jwks_view, name='jwks_view'),
    
]