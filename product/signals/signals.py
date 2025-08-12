import random
from django.db.models.signals import pre_save
from django.dispatch import receiver

from product.models import Product


@receiver(pre_save, sender=Product)
def generate_product_code(sender, instance, **kwargs):
    """
    Mahsulot saqlanishidan oldin unga unique kod generatsiya qilish
    """
    if not instance.code:
        max_attempts: int  = 100
        for attempt in range(max_attempts):
            new_code = str(random.randint(100000, 999999))  # 6 xonali raqam
            if not Product.objects.filter(code=new_code).exists():
                instance.code = new_code
                return

        raise ValueError(f"{max_attempts} urinishda unique kod generatsiya qilib bo'lmadi")