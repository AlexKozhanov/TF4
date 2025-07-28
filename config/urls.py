from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from diary.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", Home.as_view(), name="home"),
    path("diary/", include("diary.urls", namespace="diary")),
    path("users/", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
