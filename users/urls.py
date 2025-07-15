from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig


app_name = UsersConfig.name


urlpatterns = [
    # path('register/',
    #      RegisterView.as_view(
    #          template_name='idiots/register.html'),
    #      name='register'),
    # path('login/',
    #      LoginView.as_view(
    #          template_name='idiots/login.html',
    #          # next_page='../../catalog/home/'
    #      ),
    #      name='login'
    #      ),
    # path('logout/',
    #      # LoginView.as_view(next_page='catalog/home.html'),
    #      LogoutView.as_view(
    #          template_name='idiots/login.html',
    #          # template_name=''
    #          next_page='../../catalog/home/',
    #          # next_page=''
    #      ),
    #      name='logout'
    #      ),
]