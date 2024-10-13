from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Подключаем маршруты приложения `api`
    path('api/auth/', include('djoser.urls')),  # Маршруты Djoser
    path('api/auth/', include('djoser.urls.jwt')),  # Маршруты JWT
]
