from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .users import User
from .serializers import SignupSerializer


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