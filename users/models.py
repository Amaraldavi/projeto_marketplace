from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIPO_USUARIO = (
        ('ADMIN', 'Administrador'),
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO)