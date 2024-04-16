from django.shortcuts import redirect

from .services import PurchaseService


def purchase(request):
    purchase_service = PurchaseService()
    purchase_service.perform_purchase(request.user)
    return redirect('order')
