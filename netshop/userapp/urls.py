
from django.contrib import admin
from django.urls import path,include
from userapp import views

urlpatterns = [
    path('register/',views.Register.as_view()),
    path('center/',views.userCenter),
    path('login/',views.LoginView.as_view()),
    path('loadCode/',views.loadCode),
    path('checkcode/',views.checkcode),
    path('loginout/',views.loginout),
    path('address/',views.AddressView.as_view()),
    path('loadArea/',views.loadArea),
    path('updateDefaultAddr/',views.updateDefaultAddrView),
    
]


