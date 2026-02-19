from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # AUTH
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    #Captiva
    path('model/captiva/', views.captiva_detail, name='captiva_detail'),
    path('model/tracker/', views.tracker_detail, name='tracker_detail'),
    path('model/traverse/', views.traverse_detail, name='traverse_detail'),
    path('model/onix/', views.onix_detail, name='onix_detail'),
path('model/tahoe/', views.tahoe_detail, name='tahoe_detail'),

    #avtomobillar
    path('avtomobillar/', views.cars_list, name='cars_list'),
    path('avtomobillar/captiva/', views.captiva_config, name='captiva_config'),
    path('avtomobillar/onix/', views.onix_config, name='onix_config'),
path('avtomobillar/tracker/', views.tracker_config, name='tracker_config'),
path('avtomobillar/tahoe/', views.tahoe_config, name='tahoe_config'),
path('avtomobillar/labo/', views.labo_config, name='labo_config'),
path('avtomobillar/damas/', views.damas_config, name='damas_config'),
    path("buy/", views.buy_car, name="buy_car"),
    path("chat/", views.chat, name="chat"),
]
