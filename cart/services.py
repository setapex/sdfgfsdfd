from django.db.models import F
from django.http import Http404

from products.models import Product
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


class CartService(ModelService):
    def add_item_to_cart(self, user, product_id, quantity):
        product = None
        try:
            product = self.get_item(Product, pk=product_id)
            cart = self.get_item(Cart, user=user)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        except Cart.DoesNotExist:
            cart = self.create_item(Cart, user=user)

        cart_item = self.get_queryset(CartItem, cart=cart, product=product).first()

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            self.create_item(CartItem, cart=cart, product=product, quantity=quantity)

    def get_cart_items(self, user):
        return self.get_queryset(CartItem, cart__user=user)

    @staticmethod
    def calculate_total(cart_items):
        return sum(item.total_price for item in cart_items)

    def delete_item_from_cart(self, item_id, user):
        try:
            cart_item = self.get_item(CartItem, id=item_id, cart__user=user)
        except CartItem.DoesNotExist:
            raise Http404("Product does not exist")

        self.delete_item(cart_item)
