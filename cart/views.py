from django.http import JsonResponse
from django.shortcuts import redirect, render

from .services import PurchaseService, CartService

cart_service = CartService()


def purchase(request):
    purchase_service = PurchaseService()
    purchase_service.perform_purchase(request.user)
    return redirect('order')


def add_to_cart(request, product_id):
    quantity = int(request.GET.get('product-quanity'))
    cart_service.add_item_to_cart(request.user, product_id, quantity)
    return redirect('order')


def cart_view(request):
    cart_items = cart_service.get_cart_items(request.user)
    total_price = cart_service.calculate_total(cart_items)
    return render(request, 'cart/order.html',
                  {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, item_id):
    cart_service.delete_item_from_cart(item_id, request.user)
    return JsonResponse({'message': 'Success'})
