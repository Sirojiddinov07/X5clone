from rest_framework import viewsets, status
from rest_framework.response import Response
from product.serializer import ShopSerializer
from product.services import ShopService


class ShopViewSet(viewsets.ViewSet):
    def list(self, request):
        shops = ShopService.get_all_shops()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        shop = ShopService.get_shop_by_id(pk)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def create(self, request):
        serializer = ShopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop = ShopService.create_shop(serializer.validated_data)
        return Response(ShopSerializer(shop).data, status=status.HTTP_201_CREATED)


