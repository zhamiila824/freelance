from django.contrib.auth import authenticate, login
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from . import models
from . import serializers


class UserListView(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class UserDetailView(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)


class SignUpView(generics.CreateAPIView):
    serializer_class = serializers.UserSignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = models.User.objects.create_user(**serializer.validated_data)
            token = jwt_encode_handler(jwt_payload_handler(user))
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(views.APIView):
    serializer_class = serializers.UserSignInSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, **serializer.validated_data)
            if user:
                login(request, user)
                token = jwt_encode_handler(jwt_payload_handler(user))
                return Response({'token': token})
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


