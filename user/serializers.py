from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role')


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input-type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',
                  'role', 'balance')


class UserSignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={'input-type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')
