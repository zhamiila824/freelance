from django.urls import path
from . import views


urlpatterns = [
    path('users', views.UserListView.as_view(), name='users'),
    path('auth/sign_up', views.SignUpView.as_view(), name='sign_up'),
    path('auth/sign_in', views.SignInView.as_view(), name='login'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
]
