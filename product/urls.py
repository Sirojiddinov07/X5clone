from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.view import (
    ShopViewSet,
    ProductViewSet,
    ProductShopViewSet,
    ReplenishmentDataView,

    SaleCreateAPIView
)

router = DefaultRouter()
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-shops', ProductShopViewSet, basename='product-shop')

urlpatterns = [
    path('', include(router.urls)),
    path('sales/', SaleCreateAPIView.as_view(), name='create-sale'),
    path('replenishment-data/', ReplenishmentDataView.as_view(), name='replenishment-data'),

]