from django.urls import path

from . import views

urlpatterns = [
    path('tasks', views.TaskListView.as_view(), name='tasks'),
    path('tasks/add', views.TaskCreateView.as_view(), name='create'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
]