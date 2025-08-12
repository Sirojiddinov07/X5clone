from django.db import models
from product.models.shop import Shop
from product.models.abstrack import AbstractModel


class Product(AbstractModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True, blank=True, editable=False)
    unit = models.CharField(max_length=10)  # dona, kg, litr
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    shops = models.ManyToManyField(
        'Shop',
        through='ProductShop',
        related_name='products'
    )
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class ProductShop(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='product_shops'
    )
    shop = models.ForeignKey(
        'Shop',
        on_delete=models.CASCADE,
        related_name='shop_products'
    )
    stock = models.IntegerField(default=0)
    req_stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)


    class Meta:
        unique_together = ('product', 'shop')
        verbose_name = "Product in Shop"
        verbose_name_plural = "Products in Shops"

    def __str__(self):
        return f"{self.product.name} in {self.shop.name}"

