from rest_framework import serializers
from product.models.shop import Shop



class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
