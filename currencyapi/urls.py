from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apiapp.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)