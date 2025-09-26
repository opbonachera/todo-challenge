from django.urls import path
from .views import RegisterAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),   
]