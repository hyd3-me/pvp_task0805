from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import html
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.views.decorators.cache import never_cache

from .forms import RegistrationForm, BuyThingForm
from .models import Profile, Referral
from main_app import data_app, utils


def create_ref_link(ref_code):
    domain = 'localhost'
    return f'http://{domain}:8000{reverse(data_app.REG_PATH)}?ref={ref_code}'

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
            # messages.success(request, f'{test_data.SUCCESS_LOG}')
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
        ref = request.GET.get('ref', '')
        form = RegistrationForm()
        form.fields['ref_code'].initial = ref
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

def my_refs_view(request):
    status, refs = utils.get_referals_by_user(request.user)
    return render(request, 'my_refs.html', {'my_refs': refs})

def all_refs_view(request):
    status, refs = utils.get_all_referals()
    return render(request, 'all_refs.html', {'all_refs': refs}) 

#@never_cache
def buy_page_view(request):
    s, balance1 = utils.get_balance_by_user(request.user)
    form = BuyThingForm()
    return render(request, 'buy_page.html', {'balance': balance1, 'form': form})

def give_money_view(request):
    s, resp1 = utils.get_money(request.user)
    return redirect('buy_page')

def post_buy_view(request):
    if request.method != "POST":
        return redirect('index')
    form = BuyThingForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        s, resp1 = utils.buy_thing(request.user, amount)
        return redirect('index')
    s, balance1 = utils.get_balance_by_user(request.user)
    return render(request, 'buy_page.html', {'balance': balance1, 'form': form})