from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # tudo vem do app
    path('', include('marketplace_app.urls')),
]