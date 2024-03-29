from django.db.models import F

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
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        if request.user.role == 1:
            task = self.get_object()
            if task.done:
                return Response({'message': 'Task already done'}, status=status.HTTP_423_LOCKED)
            task.customer.pay(task.customer.id, task.price)
            request.user.get_paid(request.user.id, task.price)
            task.done = True
            task.executor = request.user
            task.save()
            return Response({'massage': 'You did task'}, status=status.HTTP_202_ACCEPTED)
        return Response({'message': 'Only executors can do tasks'}, status=status.HTTP_403_FORBIDDEN)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = serializers.CreateTaskSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if request.user.role == 0:
            if serializer.is_valid():
                validated_data = serializer.validated_data
                if validated_data.get('price') > (request.user.balance - request.user.promised_balance):
                    return Response({'message': 'Not enough money on balance'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                models.Task.objects.create(
                    title=validated_data.get('title'),
                    description=validated_data.get('description'),
                    price=validated_data.get('price'),
                    customer=request.user
                )
                request.user.promised_balance = F('promised_balance') + validated_data.get('price')
                request.user.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Only customers can create tasks'}, status=status.HTTP_403_FORBIDDEN)
