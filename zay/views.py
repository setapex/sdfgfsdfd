from random import sample

from django.shortcuts import render, get_object_or_404, redirect
from django_filters.views import FilterView

from cart.models import CartItem, Cart
from products.models import Product
from .filters import ProductFilter


def index(request):
    random_products = sample(list(Product.objects.all()), 3)
    context = {
        'random_products': random_products,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def cart_view(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    return render(request, 'order.html', {'cart_items': cart_items})


def add_to_cart(request, product_id):
    print(f"Adding product with ID {product_id} to cart")
    product = get_object_or_404(Product, pk=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        quantity=request.GET.get('product-quanity', 1)
    )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    print('END')

    return redirect('order')


def purchase(request):
    cart = Cart.objects.get(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    for cart_item in cart_items:
        if cart_item.product.quantity >= cart_item.quantity:
            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()

            cart_item.delete()
        else:
            print("Sorry, not enough stock available for cart_item.product.name", cart_item.product.name)

    cart_items.delete()
    print("Purchase successful! Thank you for shopping with us.")

    return redirect('order')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop-single.html', {'product': product})


class ProductListView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'shop.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        gender = self.request.GET.get('gender')
        unit = self.request.GET.get('unit')

        if gender:
            queryset = queryset.filter(gender=gender)
        if unit:
            queryset = queryset.filter(unit=unit)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context
