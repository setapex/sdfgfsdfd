from django.contrib import admin

from .models import Cart, PurchaseItem

admin.site.register(Cart)
admin.site.register(PurchaseItem)