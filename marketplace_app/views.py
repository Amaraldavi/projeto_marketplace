from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import models
from django.contrib import messages
from .forms import ListingForm
from .models import Listing, ListingImage, Category, StoreProfile, CommonProfile


def home(request):
    # Últimos produtos para o carrossel (últimos 5 criados)
    carousel_products = Listing.objects.prefetch_related('images').filter(status='active').order_by('-created_at')[:5]

    # Destaques: anúncios patrocinados ou de lojas
    featured_products = Listing.objects.prefetch_related('images').filter(
        status='active'
    ).filter(
        models.Q(is_featured=True) | models.Q(is_store_featured=True)
    ).order_by('-created_at')[:12]

    # Todos os anúncios (exceto os já mostrados no carrossel e destaques)
    all_products = Listing.objects.prefetch_related('images').filter(status='active').exclude(
        id__in=[p.id for p in carousel_products] + [p.id for p in featured_products]
    ).order_by('-created_at')

    # Categorias cadastradas
    categories = Category.objects.all()

    context = {
        'carousel_products': carousel_products,
        'featured_products': featured_products,
        'anuncios': all_products,
        'categories': categories,
    }

    return render(request, 'home.html', context)


@login_required
def criar_anuncio(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.seller = request.user
            anuncio.save()

            # Processar imagem
            image = request.FILES.get('image')
            if image:
                ListingImage.objects.create(listing=anuncio, image=image)

            return redirect('home')
    else:
        form = ListingForm(user=request.user)

    return render(request, 'marketplace_app/criar_anuncio.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
            else:
                request.session.set_expiry(0)  # Browser session
            return redirect('home')
        else:
            messages.error(request, 'Credenciais inválidas.')

    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def user_register(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')

        if account_type == 'individual':
            # Criar usuário pessoa física
            User = get_user_model()
            user = User.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                is_store=False
            )

            # Criar perfil comum
            CommonProfile.objects.create(
                user=user,
                cpf=request.POST.get('cpf')
            )

            messages.success(request, 'Conta criada com sucesso! Faça o login.')
            return redirect('login')

        elif account_type == 'store':
            # Criar usuário loja
            User = get_user_model()
            user = User.objects.create_user(
                username=request.POST.get('store_username'),
                email=request.POST.get('store_email'),
                password=request.POST.get('store_password'),
                first_name=request.POST.get('responsible_name'),
                is_store=True
            )

            # Criar perfil de loja
            StoreProfile.objects.create(
                user=user,
                cnpj=request.POST.get('cnpj'),
                razao_social=request.POST.get('company_name'),
                verified=False
            )

            messages.success(request, 'Conta de loja criada com sucesso! Aguarde verificação.')
            return redirect('login')

    return render(request, 'users/register.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_store = request.POST.get('is_store') == 'on'

        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            is_store=is_store
        )

        login(request, user)
        return redirect('home')

    return render(request, 'users/register.html')