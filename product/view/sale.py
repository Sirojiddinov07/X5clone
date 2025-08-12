# views.py
from rest_framework import generics
from product.services.sale import SaleService
from product.serializer.sale import SaleSerializer
from rest_framework.response import Response
from django.core.exceptions import ValidationError


class SaleCreateAPIView(generics.CreateAPIView):
    serializer_class = SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sale = SaleService.create_sale(
                shop_id=serializer.validated_data['shop'].id,
                items=serializer.validated_data['items'],
                payment_method=serializer.validated_data.get('payment_method', 'cash')
            )
            return Response(SaleSerializer(sale).data, status=201)

        except ValidationError as e:
            return Response({"error": str(e)}, status=400)