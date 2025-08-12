from django.contrib import admin
from django.db.models import Sum
from product.models.product import  Product, ProductShop

class ProductShopInline(admin.TabularInline):
    model = ProductShop
    fk_name = 'product'
    extra = 1
    fields = ('shop', 'stock', 'req_stock', 'sold')
    autocomplete_fields = ['shop']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'unit', 'purchase_price', 'selling_price',
                   'shop_count', 'total_stock', 'total_sold')
    search_fields = ('name', 'code')
    list_filter = ('unit',)
    inlines = [ProductShopInline]

    def shop_count(self, obj):
        return obj.product_shops.count()  # productshop_set -> product_shops

    shop_count.short_description = 'Doʻkonlar soni'

    def total_stock(self, obj):
        result = obj.product_shops.aggregate(total=Sum('stock'))  # productshop_set -> product_shops
        return result['total'] or 0

    total_stock.short_description = 'Umumiy zaxira'

    def total_sold(self, obj):
        result = obj.product_shops.aggregate(total=Sum('sold'))  # productshop_set -> product_shops
        return result['total'] or 0

    total_sold.short_description = 'Umumiy sotilgan'

@admin.register(ProductShop)
class ProductShopAdmin(admin.ModelAdmin):
    list_display = ('product', 'shop', 'stock', 'req_stock', 'sold', 'need_restock')
    list_select_related = ('product', 'shop')
    search_fields = ('product__name', 'shop__name')
    list_filter = ('shop',)
    autocomplete_fields = ['product', 'shop']
    list_editable = ('stock', 'req_stock')
    actions = ['restock_action']

    def need_restock(self, obj):
        return obj.stock < obj.req_stock

    need_restock.boolean = True
    need_restock.short_description = 'Zaxira talab qilinadi'

    @admin.action(description='Tanlanganlarni zaxirani toʻldirish')
    def restock_action(self, request, queryset):
        for item in queryset:
            needed = item.req_stock - item.stock
            if needed > 0:
                item.stock += needed
                item.save()
        self.message_user(request, f"{queryset.count()} ta mahsulot zaxirasi toʻldirildi")