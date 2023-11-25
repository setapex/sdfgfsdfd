from django.contrib import admin
from django.urls import path

from zay import views
from zay.views import ProductListView

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('shop', ProductListView.as_view(), name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin/', admin.site.urls),
    path('reg', views.reg, name='re'),
]