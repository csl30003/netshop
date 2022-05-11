#coding=utf-8

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('checkUname/', views.CheckUnameView.as_view()),
    path('center/', views.CenterView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('loadCode.jpg', views.LoadCodeView.as_view()),
    path('checkcode/', views.CheckCodeView.as_view()),
    path('address/', views.AddressView.as_view()),
    path('loadArea/', views.LoadAreaView.as_view()),
]