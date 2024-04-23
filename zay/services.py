from datetime import datetime
import math
from django.db.models import Sum

from cart.models import PurchaseItem
from products.models import Product
from aft.model_service import ModelService


def control_products(start_date_str, end_date_str, number):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    purchase_sum_per_product = (ModelService.get_queryset(PurchaseItem, purchase_date__range=(start_date, end_date))
                                .values('product__name', 'product__price').annotate(total_quantity=Sum('quantity')))
    purchase_info_dict = {data['product__name']: data['total_quantity'] for data in purchase_sum_per_product}
    purchases_info_dict = {data['product__name']: data['product__price'] for data in purchase_sum_per_product}

    k = 50
    h = 0.02
    l = 5
    le = l
    q = int(number)
    discount = 0.3
    result_list = []

    for product in Product.objects.all():
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
            if q < ym or q > q_big:
                total_pursh = ym
            else:
                total_pursh = q
            if ym > q:
                total_price = total_pursh * c2
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
                    'isDiscount': False,
                    'q': q
                })
    return result_list