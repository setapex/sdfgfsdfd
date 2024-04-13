from django.contrib import admin

from .models import Cart, PurchaseItem, Purchase

admin.site.register(Cart)
admin.site.register(PurchaseItem)
admin.site.register(Purchase)