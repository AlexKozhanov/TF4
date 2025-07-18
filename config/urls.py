from django.contrib import admin
from django.urls import include, path
from diary.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Home.as_view(), name="home"),
    path("diary/", include("diary.urls", namespace="diary")),
    path("users/", include("users.urls", namespace="users")),
]
