import math
from random import sample

from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django_filters.views import FilterView

from cart.models import CartItem, Cart, Purchase, PurchaseItem
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
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'order.html', {'cart_items': cart_items, 'total_price': total_price})


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

    purchase = Purchase.objects.create(user=request.user)

    for cart_item in cart_items:
        if cart_item.product.quantity >= cart_item.quantity:
            # Проверяем, существует ли запись для этого продукта у пользователя
            purchase_item, created = PurchaseItem.objects.get_or_create(
                purchase=purchase,
                product=cart_item.product,
                defaults={'quantity': 0}  # Устанавливаем количество в 0 при создании новой записи
            )

            # Обновляем количество продукта в записи
            PurchaseItem.objects.filter(pk=purchase_item.pk).update(
                quantity=F('quantity') + cart_item.quantity
            )

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
        sizes = self.request.GET.get('sizes')
        if gender:
            queryset = queryset.filter(gender=gender)
        if unit:
            queryset = queryset.filter(unit=unit)
        if sizes:
            queryset = queryset.filter(sizes__contains=sizes)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context


@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return JsonResponse({'message': 'Success'})

def control(request):
    purchase_sum_per_product = PurchaseItem.objects.values('product__name').annotate(total_quantity=Sum('quantity'))
    purchase_info_dict = {data['product__name']: data['total_quantity'] for data in purchase_sum_per_product}

    k = 50
    h = 0.02
    l = 5
    le = l
    prod = Product.objects.all()

    result_list = []

    for product in prod:
        product.total_quantity = purchase_info_dict.get(product.name, 0)
        d = product.total_quantity
        if d > 0:
            y = int((2 * k * d / h) ** 0.5)
            t = int(y / d)
            if l > t:
                le = l - math.floor(l / t) * t
            quant = le * d
            print(product)
            print(quant)

            if quant > product.quantity:
                print(f'quant = {quant} > quantity = {product.quantity} ')
                result_list.append({
                    'product': product,
                    'quant': quant,
                    'quantity': product.quantity,
                    'image_url': product.image1_url,
                    'prod_need': y
                })

    context = {
        'products': result_list
    }
    print(context)
    return render(request, 'control-products.html', context)
