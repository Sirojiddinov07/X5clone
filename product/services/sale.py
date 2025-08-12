from django.db import transaction
from product.models import Sale, SaleItem, ProductShop
from django.core.exceptions import ValidationError


class SaleService:
    @staticmethod
    @transaction.atomic
    def create_sale(shop_id, items, **kwargs):
        """
        Yangi sotuv yaratish
        :param shop_id: Do'kon IDsi (int)
        :param items: Mahsulotlar ro'yxati [{"product_id": 1, "quantity": 2}]
        :param kwargs: Qo'shimcha maydonlar (customer_name, payment_method, ...)
        :return: Sale object
        """
        sale_items = []
        total_amount = 0

        # 1. Validatsiya va zaxirani tekshirish
        for item in items:
            try:
                # Product ID ni olish (ikkala formatni qo'llab-quvvatlash)
                product_id = item.get('product_id') or item.get('product')
                if not product_id:
                    raise ValidationError("product_id is required")

                # Quantity ni tekshirish
                quantity = item['quantity']
                if quantity <= 0:
                    raise ValidationError(f"Quantity must be positive for product {product_id}")

                # Mahsulot do'konda mavjudligini tekshirish
                product_shop = ProductShop.objects.select_related('product').get(
                    shop_id=shop_id,
                    product_id=product_id
                )

                # Zaxira yetarli ekanligini tekshirish
                if product_shop.stock < quantity:
                    raise ValidationError(
                        f"Not enough stock for product {product_id}. "
                        f"Available: {product_shop.stock}, Requested: {quantity}"
                    )

            except KeyError as e:
                raise ValidationError(f"Missing required field: {str(e)}")
            except ProductShop.DoesNotExist:
                raise ValidationError(f"Product {product_id} not available in shop {shop_id}")

        # 2. Sotuvni yaratish
        sale = Sale.objects.create(shop_id=shop_id, **kwargs)

        # 3. Sotuv elementlari va zaxira yangilash
        for item in items:
            product_id = item.get('product_id') or item.get('product')
            quantity = item['quantity']

            product_shop = ProductShop.objects.select_related('product').get(
                shop_id=shop_id,
                product_id=product_id
            )

            # Sotuv elementini yaratish
            sale_item = SaleItem(
                sale=sale,
                product_id=product_id,
                quantity=quantity,
                unit_price=product_shop.product.selling_price,
                total_price=product_shop.product.selling_price * quantity
            )
            sale_items.append(sale_item)

            # Zaxirani yangilash
            product_shop.stock -= quantity
            product_shop.sold += quantity
            product_shop.save()

            total_amount += sale_item.total_price

        # 4. Sotuv elementlarini saqlash
        SaleItem.objects.bulk_create(sale_items)

        # 5. Umumiy summani yangilash
        sale.total_amount = total_amount
        sale.save()

        return sale