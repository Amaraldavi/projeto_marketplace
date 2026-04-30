from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django auth URLs (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # tudo vem do app
    path('', include('marketplace_app.urls')),
]

# Servir arquivos de mídia e estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) if hasattr(settings, 'STATIC_ROOT') else []