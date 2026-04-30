from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('criar-anuncio/', views.criar_anuncio, name='criar_anuncio'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
]