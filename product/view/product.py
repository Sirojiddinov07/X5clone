from rest_framework import viewsets, status
from rest_framework.response import Response
from product.serializer import ProductSerializer, ProductShopSerializer
from product.services import ProductService, ProductShopService


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = ProductService.get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = ProductService.get_product_by_id(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = ProductService.create_product(serializer.validated_data)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductShopViewSet(viewsets.ViewSet):
    def list(self, request):
        product_shops = ProductShopService.get_all_product_shops()
        serializer = ProductShopSerializer(product_shops, many=True)
        return Response(serializer.data)

    def retrieve(self, request):
        product_id = request.query_params.get('product_id')
        shop_id = request.query_params.get('shop_id')
        product_shop = ProductShopService.get_product_shop_by_ids(product_id, shop_id)
        serializer = ProductShopSerializer(product_shop)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductShopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_shop = ProductShopService.create_product_shop(serializer.validated_data)
        return Response(ProductShopSerializer(product_shop).data, status=status.HTTP_201_CREATED)


