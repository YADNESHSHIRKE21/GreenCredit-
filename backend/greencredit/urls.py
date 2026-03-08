from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/verification/', include('verification.urls')),
    path('api/verdant/', include('verdant.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/recognition/', include('recognition.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)