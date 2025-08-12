from django.db.models import QuerySet
from product.models import Product, ProductShop



class ProductService:
    @staticmethod
    def get_all_products() -> QuerySet[Product]:
        """Returns all products."""
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(pk: int) -> Product:
        """Returns single product by ID."""
        return Product.objects.get(pk=pk)

    @staticmethod
    def create_product(data: dict) -> Product:
        """Creates new product."""
        return Product.objects.create(**data)


class ProductShopService:
    @staticmethod
    def get_all_product_shops() -> QuerySet[ProductShop]:
        """Returns all product-shop relations."""
        return ProductShop.objects.all()

    @staticmethod
    def get_product_shop_by_ids(product_id: int, shop_id: int) -> ProductShop:
        """Returns single product-shop relation."""
        return ProductShop.objects.get(product_id=product_id, shop_id=shop_id)

    @staticmethod
    def create_product_shop(data: dict) -> ProductShop:
        """Creates new product-shop relation."""
        return ProductShop.objects.create(**data)

