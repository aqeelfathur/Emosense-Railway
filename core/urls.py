from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('auth/', include('users.urls')),
    path('', include('emotion.urls')),
    path('history/', include('history.urls')),
]