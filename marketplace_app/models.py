from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    TIPO_ANUNCIO = (
        ('VENDA', 'Venda'),
        ('TROCA', 'Troca'),
    )

    CONDICAO = (
        ('NOVO', 'Novo'),
        ('USADO', 'Usado'),
    )

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_ANUNCIO)
    condicao = models.CharField(max_length=10, choices=CONDICAO)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='listings/')