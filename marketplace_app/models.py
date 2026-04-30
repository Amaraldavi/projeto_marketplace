from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    is_store = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class StoreProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.razao_social


class CommonProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Listing(models.Model):
    SALE = 'sale'
    TRADE = 'trade'

    LISTING_TYPE_CHOICES = [
        (SALE, 'Venda'),
        (TRADE, 'Troca'),
    ]

    NEW = 'new'
    USED = 'used'

    CONDITION_CHOICES = [
        (NEW, 'Novo'),
        (USED, 'Usado'),
    ]

    ACTIVE = 'active'
    PAUSED = 'paused'
    SOLD = 'sold'

    STATUS_CHOICES = [
        (ACTIVE, 'Ativo'),
        (PAUSED, 'Pausado'),
        (SOLD, 'Vendido'),
    ]

class Listing(models.Model):
    SALE = 'sale'
    TRADE = 'trade'

    LISTING_TYPE_CHOICES = [
        (SALE, 'Venda'),
        (TRADE, 'Troca'),
    ]

    NEW = 'new'
    USED = 'used'

    CONDITION_CHOICES = [
        (NEW, 'Novo'),
        (USED, 'Usado'),
    ]

    ACTIVE = 'active'
    PAUSED = 'paused'
    SOLD = 'sold'

    STATUS_CHOICES = [
        (ACTIVE, 'Ativo'),
        (PAUSED, 'Pausado'),
        (SOLD, 'Vendido'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)

    # Novos campos para destaques
    is_featured = models.BooleanField(default=False, help_text="Anúncio patrocinado")
    is_store_featured = models.BooleanField(default=False, help_text="Destaque para anúncios de loja")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.seller.is_store and self.listing_type == self.TRADE:
            raise ValueError("Lojas não podem criar anúncios de troca.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.seller.is_store and self.listing_type == self.TRADE:
            raise ValueError("Lojas não podem criar anúncios de troca.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')

    def __str__(self):
        return f"Imagem de {self.listing.title}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"