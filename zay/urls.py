from django.contrib import admin
from django.urls import path, include

from zay import views
from zay.views import ProductListView

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('aft.urls')),
    path('about', views.about, name='about'),
    path('shop', ProductListView.as_view(), name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin/', admin.site.urls),
]
