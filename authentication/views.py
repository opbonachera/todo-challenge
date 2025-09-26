from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from .serializers import RegisterSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully.'})

class LoginAPIView(APIView):
    permission_classes = [] 
    
    def post(self, request):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already logged in.'})

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response(user)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})