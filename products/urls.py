from django.urls import path

from products.views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='shop'),
    path('<int:product_id>/', product_detail, name='product_detail'),
]
