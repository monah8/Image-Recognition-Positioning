from django.contrib import admin
from django.urls import path
from core.views import get_coordinates

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('coords/<str:file_name>', get_coordinates, name='get_coordinates'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )