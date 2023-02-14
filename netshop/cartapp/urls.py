
from django.contrib import admin
from django.urls import path,include
from cartapp import views

urlpatterns = [
    path('cartview/',views.cartview),
    path('queryAll/',views.queryAll),

    
]


