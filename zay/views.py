from random import sample

from django.shortcuts import render

from products.models import Product
from zay.services import control_products


def index(request):
    random_products = sample(list(Product.objects.all()), 3)
    context = {
        'random_products': random_products,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def control(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    number = request.POST.get('number', 200)
    products = control_products(start_date, end_date, number)
    context = {'products': products}
    return render(request, 'control-products.html', context)


def input_number(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        if number is not None:
            return render(request, 'pass_opt.html', {'number': number})
        else:
            pass
    return render(request, 'pass_opt.html')
