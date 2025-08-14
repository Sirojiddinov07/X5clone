from django.core.management.base import BaseCommand
from product.models import Product, ProductShop, Shop
from faker import Faker
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Faker yordamida 100 ta realistik mahsulotlar yaratish'

    def handle(self, *args, **options):
        fake = Faker()

        # Do'konlarni olish
        shops = Shop.objects.filter(id__in=[1, 2, 3])
        if not shops.exists():
            self.stdout.write(self.style.ERROR('1, 2, 3 IDli do\'konlar topilmadi'))
            return

        # Mahsulot turlari va o'lchov birliklari
        categories = {
            'Elektronika': ['dona'],
            'Maishiy texnika': ['dona'],
            'Kiyim-kechak': ['dona'],
            'Oziq-ovqat': ['kg', 'litr', 'dona'],
            'Qurilish materiallari': ['kg', 'litr', 'dona']
        }

        for i in range(1, 101):
            # Tasodifiy kategoriya va o'lchov birligini tanlash
            category = random.choice(list(categories.keys()))
            unit = random.choice(categories[category])

            # Mahsulot nomini generatsiya qilish
            if category == 'Elektronika':
                name = f"{fake.word().capitalize()} {random.choice(['smart', 'pro', 'mini', 'max', 'air'])} {fake.random_element(['phone', 'pad', 'book', 'watch', 'pod'])}"
            elif category == 'Maishiy texnika':
                name = f"{fake.company()} {fake.random_element(['sovutgich', 'mikroto\'lqinli pech', 'changyutgich', 'kir yuvish mashinasi'])}"
            elif category == 'Kiyim-kechak':
                name = f"{fake.color_name().capitalize()} {fake.random_element(['ko\'ylak', 'shim', 'futbolka', 'kurtka', 'tufli'])}"
            elif category == 'Oziq-ovqat':
                name = f"{fake.word().capitalize()} {fake.random_element(['non', 'sut', 'guruch', 'yog\'', 'gosht', 'meva'])}"
            else:
                name = f"{fake.word().capitalize()} {fake.random_element(['bo\'yoq', 'sement', 'plastik', 'truba', 'plyonka'])}"

            # Narxlarni generatsiya qilish
            purchase_price = Decimal(random.uniform(1, 1000)).quantize(Decimal('0.01'))
            selling_price = (purchase_price * Decimal(random.uniform(1.1, 2.0))).quantize(Decimal('0.01'))

            # Mahsulot yaratish
            product = Product.objects.create(
                name=name,
                unit=unit,
                purchase_price=purchase_price,
                selling_price=selling_price
            )

            # Har bir do'konga mahsulotni joylashtirish
            for shop in shops:
                req_stock = random.randint(0, 100)
                ProductShop.objects.create(
                    product=product,
                    shop=shop,
                    req_stock=req_stock,
                    stock=random.randint(0, req_stock),  # req_stock har doim stockdan <=
                    sold=random.randint(0, 200)
                )

            self.stdout.write(self.style.SUCCESS(f'{i}/100 - {name} yaratildi'))

        self.stdout.write(self.style.SUCCESS('100 ta mahsulot muvaffaqiyatli yaratildi!'))