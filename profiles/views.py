from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status, permissions, authentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .users import User
from .serializers import SignupSerializer
from rest_framework.views import APIView

class SignupView(generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        data = request.data 
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        obj = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        
        return Response(data=obj, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            obj = {
                'message': 'Login successful',
                'token': token.key
            }
            
            return Response(data=obj, status=status.HTTP_200_OK)
        return Response(data={
            'message': 'Email or password incorrect',
        }, status=status.HTTP_400_BAD_REQUEST)