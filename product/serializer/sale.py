# serializers.py
from rest_framework import serializers
from product.models.sale import Sale, SaleItem
from product.serializer import ProductSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)  # Yangi qator
    product = ProductSerializer(read_only=True)  # Agar mahsulot ma'lumotlari ham kerak bo'lsa

    class Meta:
        model = SaleItem
        fields = ['product', 'product_id', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['unit_price', 'total_price', 'product']  # product qo'shil



class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'shop', 'total_amount', 'sale_date',  'payment_method', 'items']
        read_only_fields = ['total_amount', 'sale_date']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one product is required")
        return value