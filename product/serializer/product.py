from rest_framework import serializers
from product.models.product import Product, ProductShop
from product.models.shop import  Shop
from product.serializer.shop import ShopSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductShopSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    shop_id = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(),
        source='shop',
        write_only=True
    )

    class Meta:
        model = ProductShop
        fields = '__all__'
        extra_kwargs = {
            'stock': {'min_value': 0},
            'req_stock': {'min_value': 0},
            'sold': {'min_value': 0}
        }