from django.urls import path
from .views import criar_anuncio

urlpatterns = [
    path('criar/', criar_anuncio, name='criar_anuncio'),
]