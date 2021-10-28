from django.contrib import admin
from mainapp.models import ProductsCategory, Product
from authapp.models import ShopUser


admin.site.register(ProductsCategory)
admin.site.register(Product)
admin.site.register(ShopUser)
