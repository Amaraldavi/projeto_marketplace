from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIPO_USUARIO = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    tipo = models.CharField(max_length=2, choices=TIPO_USUARIO)

    def is_pf(self):
        return self.tipo == 'PF'

    def is_pj(self):
        return self.tipo == 'PJ'
    
class CommonProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return f"PF - {self.user.username}"


class StoreProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=255)
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return f"PJ - {self.razao_social}"    