from django.contrib import admin
from django.urls import path, include

from zay import views
from zay.views import ProductListView

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', include('aft.urls')),
    path('about', views.about, name='about'),
    path('shop', ProductListView.as_view(), name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin/', admin.site.urls, name='admin'),
    path('order', views.cart_view, name='order'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('purchase/', views.purchase, name='purchase'),
    path('control/', views.control, name='control'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('input_opt/', views.input_number, name='input_opt')
]

