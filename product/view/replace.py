from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from product.models.product import ProductShop

class ReplenishmentDataView(APIView):
    def get(self, request):
        shops_data = {}

        product_shops = ProductShop.objects.filter(
            stock__lt=F('req_stock')
        ).select_related('shop', 'product')

        for ps in product_shops:
            shop_id = ps.shop.id
            if shop_id not in shops_data:
                shops_data[shop_id] = {
                    'shop_name': ps.shop.name,
                    'products': []
                }

            needed = ps.req_stock - ps.stock
            shops_data[shop_id]['products'].append({
                'product_code': ps.product.code,
                'product_name': ps.product.name,
                'current_stock': ps.stock,
                'required': ps.req_stock,
                'needed': needed,
                'unit': ps.product.unit
            })

        return Response(shops_data, status=status.HTTP_200_OK)