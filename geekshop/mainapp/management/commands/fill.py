import json
from django.conf import settings
from django.core.management.base import BaseCommand
from authapp.models import ShopUser
from mainapp.models import ProductsCategory, Product


def load_from_json(file_name):
    with open(f'{settings.BASE_DIR}/geekshop/json/{file_name}.json', encoding='UTF-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json("categories")
        ProductsCategory.objects.all().delete()

        for category in categories:
            ProductsCategory.objects.create(**category)

        products = load_from_json("products")
        Product.objects.all().delete()

        for product in products:
            category_name = product["category"]
            category_item = ProductsCategory.objects.get(name=category_name)
            product["category"] = category_item
            Product.objects.create(**product)

    ShopUser.objects.create_superuser(username='django', password='geekbrains', age=32)
