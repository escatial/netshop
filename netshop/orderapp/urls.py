from django.contrib import admin
from django.urls import path,include
from orderapp import views

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('toOrder/', views.toOrder),
    path('toPay/', views.toPay),
    path('checkPay/', views.checkPay),

]