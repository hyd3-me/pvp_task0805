from django.urls import path, include, reverse
from . import views
from main_app import data_app


urlpatterns = [
    path('',        views.index_view, name=data_app.HOME_PATH),
    path('login',   views.login_view, name=data_app.LOGIN_PATH),
    path('logout',  views.logout_view, name=data_app.LOGOUT_PATH),
    path('register', views.register, name=data_app.REG_PATH),
    path('profile/', views.profile, name=data_app.PROFILE_PATH),
    ]
