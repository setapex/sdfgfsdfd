from django.db.models import Q
from django.http import Http404

from products.model_service import ModelService
from products.models import Product


class ProductService(ModelService):
    @staticmethod
    def apply_filters(queryset, query, genders, units, categories, sizes):
        query_search = Q(name__icontains=query) | Q(brand__icontains=query) if query else Q()
        gender_filters = Q(gender__in=genders) if genders else Q()
        unit_filters = Q(unit__in=units) if units else Q()
        category_filters = Q(category__in=categories) if categories else Q()
        size_filters = Q()
        for size in sizes:
            size_filters |= Q(sizes__contains=size)

        return queryset.filter(query_search & gender_filters & unit_filters & category_filters & size_filters)
    @staticmethod
    def get_product_details(product_id):
        try:
            product = ModelService.get_item(Product, id=product_id)
        except Product.DoesNotExist:
            raise Http404('Product does not exist')

        return product
