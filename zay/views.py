import math
from datetime import datetime
from random import sample

from django.db.models import Sum, Q
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


"""
контроллер

слой сервисов

абстракция над моделями

модели

"""


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop-single.html', {'product': product})


class ProductListView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'shop.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        genders = self.request.GET.getlist('gender')
        units = self.request.GET.getlist('unit')
        categories = self.request.GET.getlist('category')
        sizes = self.request.GET.getlist('sizes')

        gender_filters = Q(gender__in=genders) if genders else Q()
        unit_filters = Q(unit__in=units) if units else Q()
        category_filters = Q(category__in=categories) if categories else Q()
        size_filters = Q()
        for size in sizes:
            size_filters |= Q(sizes__contains=size)

        queryset = queryset.filter(gender_filters & unit_filters & category_filters & size_filters)

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
    start_date_str = request.POST.get('start_date')
    end_date_str = request.POST.get('end_date')
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    purchase_sum_per_product = (PurchaseItem.objects.filter(purchase_date__range=(start_date, end_date))
                                .values('product__name', 'product__price').annotate(total_quantity=Sum('quantity')))
    purchase_info_dict = {data['product__name']: data['total_quantity'] for data in purchase_sum_per_product}
    purchases_info_dict = {data['product__name']: data['product__price'] for data in purchase_sum_per_product}
    print(purchase_info_dict)

    k = 50
    h = 0.02
    l = 5
    le = l
    number = int(request.POST.get('number', 200))
    q = number
    print(q)
    discount = 0.3  # наименьшая скидка
    total_pursh = 0
    total_price = 0
    isDiscount = False
    prod = Product.objects.all()

    result_list = []

    for product in prod:

        product.total_quantity = purchase_info_dict.get(product.name, 0)
        product.price = purchases_info_dict.get(product.name, 0)
        c1 = float(product.price)
        c2 = float(product.price) * (1 - discount)
        d = product.total_quantity
        if d > 0:
            ym = int((2 * k * d / h) ** 0.5)
            t = int(ym / d)
            if l > t:
                le = l - math.floor(l / t) * t
            quant = le * d

            tcu1 = d * c1 + (k * d / ym) + h * ym / 2
            tcu2 = d * c2 + (k * d / ym) + h * ym / 2

            q_big = int(d * 10 * (c1 - c2) / (k * d + h / 2) + ym)
            print(product.name)
            print(f'{q_big} Q')
            print(f'{q} q')
            print(f'{ym} ym')
            if q < ym:
                print('ZONE 1')
            elif q >= ym and q < q_big:
                print('ZONE 2')
            elif q >= q_big:
                print('ZONE 3')
            if q < ym or q > q_big:
                total_pursh = ym
            else:
                total_pursh = q
            if ym > q:
                total_price = total_pursh * c2
                print(f'PRICE SO SKIDKOY for {product}')
            else:
                total_price = total_pursh * c1
            total_price = round(total_price, 2)
            if quant > product.quantity:
                result_list.append({
                    'product': product,
                    'quant': quant,
                    'quantity': product.quantity,
                    'image_url': product.image1_url,
                    'prod_need': total_pursh,
                    'prod_price': total_price,
                    'isDiscount': isDiscount,
                    'q': q
                })
    context = {
        'products': result_list
    }
    return render(request, 'control-products.html', context)


def input_number(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        if number is not None:
            return render(request, 'pass_opt.html', {'number': number})
        else:
            pass
    return render(request, 'pass_opt.html')


def get_profile(request):
    purchases = Purchase.objects.filter(user=request.user)
    all_items = []
    for purchase in purchases:
        items = PurchaseItem.objects.filter(purchase=purchase)
        all_items.extend(items)
    context = {
        'user': request.user,
        'purchases': purchases,
        'all_items': all_items
    }
    return render(request, 'profile.html', context)
