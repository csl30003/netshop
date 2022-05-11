# coding = utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddCartView.as_view()),
    path('queryAll/', views.CartListView.as_view()),
]
