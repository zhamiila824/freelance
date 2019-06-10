from django.shortcuts import render
from rest_framework import generics, views
from . import models
from . import serializers


class UserListView(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = serializers.UserSignUpSerializer


class LoginView(views.APIView):
    serializer_class = serializers.UserSignInSerializer

