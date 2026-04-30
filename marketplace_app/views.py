from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ListingForm
from .models import Listing


def home(request):
    anuncios = Listing.objects.all()
    return render(request, 'home.html', {'anuncios': anuncios})


@login_required
def criar_anuncio(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.seller = request.user
            anuncio.save()
            return redirect('home')
    else:
        form = ListingForm(user=request.user)

    return render(request, 'marketplace_app/criar_anuncio.html', {'form': form})
from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'users/login.html')
from django.contrib.auth.models import User
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_store = request.POST.get('is_store') == 'on'

        user = User.objects.create_user(
            username=username,
            password=password,
            is_store=is_store
        )

        login(request, user)
        return redirect('home')

    return render(request, 'users/register.html')