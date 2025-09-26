from django.urls import path
from .views import RegisterAPIView, LogoutAPIView, LoginAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='logout'), 
]