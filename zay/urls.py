from django.contrib import admin
from django.urls import path, include

from zay import views
from cart.views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('aft.urls')),
    path('order/', include("cart.urls")),
    path('about', views.about, name='about'),
    path('products/', include('products.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('control/', views.control, name='control'),
    path('input_opt/', views.input_number, name='input_opt')
]

