from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import html
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse

from .forms import RegistrationForm
from .models import Profile, Referral
from main_app import data_app, utils


def create_ref_link(ref_code):
    domain = 'localhost'
    return f'https://{domain}{reverse(data_app.REG_PATH)}?={ref_code}'

# Create your views here.

def index_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html')

def login_view(request):
    if not request.method == 'GET':
        if not request.method == 'POST':
            return redirect('index')
        form1 = AuthenticationForm(request, data=request.POST)
        if form1.is_valid():
            user1 = form1.get_user()
            login(request, user1)
            messages.success(request, f'{test_data.SUCCESS_LOG}')
            return redirect('profile')
        messages.error(request, f'form invalid. perhaps there is no such user')
    else:
        form1 = AuthenticationForm()
    return render(request, 'login.html', {'form': form1})

def logout_view(request):
    if not request.method == 'GET':
        return redirect('index')
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            ref_code = form.cleaned_data['ref_code']
            state, resp = utils.create_user((username, password, ref_code))
            user = authenticate(username=resp.username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def reg_ref(request, code):
    referrer = get_object_or_404(Profile, referral_code=code)
    if request.user.is_authenticated:
        referee = request.user
        Referral.objects.create(referrer=referrer.user, referee=referee)
    return redirect('home')

def profile(request):
    if not request.method == 'GET':
        return redirect('index')
    ref_code = utils.get_ref_code(request.user)
    ref_link = create_ref_link(ref_code)
    return render(request, 'profile.html', {'ref_link': ref_link})

