from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, EmailVerification, UserResetView, UserListView, UserUpdateView, UserDetailView, \
    UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-confirm/<str:token>/', EmailVerification.as_view(), name='email-confirm'),
    path('password-reset/', UserResetView.as_view(template_name='users/reset_form.html'), name='reset'),

    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
