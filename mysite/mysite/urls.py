from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # для регистрации и логина
    path('', include('myapp.urls')),  # основные пути приложения
]
