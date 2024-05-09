from django.urls import path, include, reverse
from . import views
from main_app import data_app


urlpatterns = [
    path('',        views.index_view, name=data_app.HOME_PATH),
    path('login',   views.login_view, name=data_app.LOGIN_PATH),
    path('logout',  views.logout_view, name=data_app.LOGOUT_PATH),
    path('register', views.register, name=data_app.REG_PATH),
    path('profile/', views.profile, name=data_app.PROFILE_PATH),

    path('my_refs/', views.my_refs_view, name=data_app.REFERRAL_PATH),
    path('all_refs/', views.all_refs_view, name=data_app.ALL_REFS_PATH),
    path('buy_page/', views.buy_page_view, name=data_app.BUY_PATH),
    path('give_money/', views.give_money_view, name=data_app.GIVE_MONEY_PATH),
    path('post_buy/', views.post_buy_view, name=data_app.POST_BUY_PATH),
    ]
