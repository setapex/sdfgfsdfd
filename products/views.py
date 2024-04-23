from django.shortcuts import render
from django_filters.views import FilterView

from products.filters import ProductFilter
from products.models import Product
from products.services import ProductService


def product_detail(request, product_id):
    product = ProductService.get_product_details(product_id)
    return render(request, 'products/shop-single.html', {'product': product})


class ProductListView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'products/shop.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        genders = self.request.GET.getlist('gender')
        units = self.request.GET.getlist('unit')
        categories = self.request.GET.getlist('category')
        sizes = self.request.GET.getlist('sizes')

        queryset = ProductService.apply_filters(queryset, query, genders, units, categories, sizes)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context