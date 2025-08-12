from django.contrib import admin
from django.utils.html import format_html
from product.models.sale import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0  # Qo'shimcha bo'sh formlar soni
    readonly_fields = ('product', 'quantity', 'unit_price', 'total_price')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False  # Yangi item qo'shishni o'chirish


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'total_amount', 'sale_date',  'payment_status', 'items_list')
    list_filter = ('shop', 'sale_date', 'payment_method')
    search_fields = ( 'shop__name',)
    date_hierarchy = 'sale_date'
    inlines = [SaleItemInline]
    readonly_fields = ('sale_date', 'total_amount')

    def items_list(self, obj):
        items = obj.items.all()[:5]  # Birinchi 5 ta mahsulotni ko'rsatish
        return ", ".join([f"{item.product.name} ({item.quantity})" for item in items])

    items_list.short_description = 'Mahsulotlar'

    def payment_status(self, obj):
        color = {
            'cash': 'green',
            'card': 'blue',
            'transfer': 'orange'
        }.get(obj.payment_method, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_payment_method_display()
        )

    payment_status.short_description = 'Toʻlov turi'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('shop').prefetch_related('items__product')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'total_price')
    list_filter = ('product',)
    search_fields = ('sale__id', 'product__name')
    raw_id_fields = ('sale', 'product')

    def has_add_permission(self, request):
        return False  # Faqat sotuv orqali qo'shish mumkin