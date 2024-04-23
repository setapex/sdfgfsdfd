from aft.model_service import ModelService
from cart.models import Purchase, PurchaseItem


class AccountService:
    @staticmethod
    def get_user_profile(user):
        purchases = ModelService.get_queryset(Purchase,user=user)
        all_items = []
        for purchase in purchases:
            items = ModelService.get_queryset(PurchaseItem, purchase=purchase)
            all_items.extend(items)
        return {'user': user, 'purchases': purchases, 'all_items': all_items}
