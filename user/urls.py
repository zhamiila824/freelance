from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('sign_in/', views.LoginView.as_view(), name='login'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user_detail')

]
