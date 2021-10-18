from SkyTech.views import home_page
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from django.conf import settings
from .settings import DEBUG
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls", namespace="user")),
    path('meeting/', include("meeting.urls", namespace="meeting")),
    path('room/', include("room.urls", namespace="room")),
    path('', home_page, name="home-page"),
]


if DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)