from django.db.models import F

from .model_service import ModelService
from .models import Cart, CartItem, Purchase, PurchaseItem


class PurchaseService(ModelService):
    def perform_purchase(self, user):
        cart = self.get_item(Cart, user=user)
        cart_items = self.get_queryset(CartItem, cart=cart)
        purchase = self.create_item(Purchase, user=user)
        for cart_item in cart_items:
            self.perform_cart_item(cart_item, purchase)
        self.delete_queryset(CartItem, cart=cart)
        print("Thank you for shopping with us.")

    def perform_cart_item(self, cart_item, purchase):
        if cart_item.product.quantity >= cart_item.quantity:
            purchase_item, created = PurchaseItem.objects.get_or_create(
                purchase=purchase,
                product=cart_item.product,
                defaults={'quantity': 0}
            )
            self.update_item(
                purchase_item,
                quantity=F('quantity') + cart_item.quantity
            )

            cart_item.product.quantity -= cart_item.quantity
            self.update_item(cart_item.product, quantity=cart_item.product.quantity)

            self.delete_item(cart_item)
        else:
            print("Sorry, not enough stock available for", cart_item.product.name)
