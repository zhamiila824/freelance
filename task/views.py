from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import serializers
from . import models


class TaskListView(generics.ListAPIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (AllowAny,)


class TaskDetailView(generics.RetrieveAPIView):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (AllowAny,)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = serializers.CreateTaskSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            models.Task.objects.create(
                title=validated_data.get('title'),
                description=validated_data.get('description'),
                price=validated_data.get('price'),
                customer=request.user
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
