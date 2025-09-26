from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework import serializers

from .serializers import LoginSerializer
from .serializers import RegisterSerializer
from core.logger import logger
class RegisterAPIView(APIView):
	permission_classes = []
	authentication_classes = []

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginAPIView(APIView):
	permission_classes = []
	authentication_classes = []

	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			token, created = Token.objects.get_or_create(user=user)
			logger.info(f'User {user.username} logged in.')
			return Response({'token': token.key}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [TokenAuthentication]

	def post(self, request):
		try:
			request.user.auth_token.delete()
		except (AttributeError, Token.DoesNotExist):
			pass
		return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError('Invalid credentials')
