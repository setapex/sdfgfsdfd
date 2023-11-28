from random import sample

from django.shortcuts import render, get_object_or_404
from django_filters.views import FilterView

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


def reg(request):
    return render(request, 'order.html')


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
