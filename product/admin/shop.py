from django.contrib import admin
from django.db.models import Sum
from product.models.shop import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone', 'product_count', 'total_stock')
    search_fields = ('name', 'location', 'phone')
    list_filter = ('location',)

    def product_count(self, obj):
        return obj.shop_products.count()  # productshop_set -> shop_products

    product_count.short_description = 'Mahsulotlar soni'

    def total_stock(self, obj):
        result = obj.shop_products.aggregate(total=Sum('stock'))  # productshop_set -> shop_products
        return result['total'] or 0

    total_stock.short_description = 'Umumiy zaxira'