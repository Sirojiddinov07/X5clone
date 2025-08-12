from django.db import models
from product.models.abstrack import AbstractModel

class Sale(AbstractModel):
    shop = models.ForeignKey('Shop', on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sale_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('transfer', "O'tkazma")
    ], default='cash')



class SaleItem(AbstractModel):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)