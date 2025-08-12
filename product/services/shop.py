from django.db.models import QuerySet
from product.models import Shop

class ShopService:
    @staticmethod
    def get_all_shops() -> QuerySet[Shop]:
        """Returns all shops."""
        return Shop.objects.all()

    @staticmethod
    def get_shop_by_id(pk: int) -> Shop:
        """Returns single shop by ID."""
        return Shop.objects.get(pk=pk)

    @staticmethod
    def create_shop(data: dict) -> Shop:
        """Creates new shop."""
        return Shop.objects.create(**data)