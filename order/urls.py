# coding=utf-8

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToOrderView.as_view()),
    path('order.html', views.OrderListView.as_view()),
    # path('topay/',views.ToPayView.as_view()),
    # path('checkPay/',views.CheckPayView.as_view()),
]
