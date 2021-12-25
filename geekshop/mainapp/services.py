import random
from mainapp.models import Product, ProductsCategory
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return products_list


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductsCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    return ProductsCategory.objects.filter(is_active=True)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    return get_object_or_404(Product, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
