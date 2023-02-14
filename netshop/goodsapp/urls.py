from django.contrib import admin
from django.urls import path,include
from goodsapp import views

urlpatterns = [
    path('', views.index),
    path('category/<int:categoryid>/page/<int:page_num>/', views.index),
    path("goodsdetails/<int:goodsid>/",views.goodsdetail),
    path("category/<int:categoryid>/",views.index),
]