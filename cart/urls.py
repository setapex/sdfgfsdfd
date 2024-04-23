from django.urls import path

from cart.views import *

urlpatterns = [
    path('', cart_view, name='order'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('purchase/', purchase, name='purchase'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]
