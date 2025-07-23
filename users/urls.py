from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from users.services import email_verification
from users.views import (
    PasswordRecoveryView, UserCreateView, UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserLoginView)

app_name = UsersConfig.name


class EmailConfirmationView:
    pass


urlpatterns = [
    path("login/", UserLoginView.as_view(template_name="registration/login.html", next_page='home'), name="login"),
    path("logout/", LogoutView.as_view(template_name='registration/login.html', next_page='../../'), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    # path("password_reset/", auth_views.PasswordResetView.as_view(), name="reset_password"),

    path("users/", UserListView.as_view(), name="user_list"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),

path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("password-recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
]