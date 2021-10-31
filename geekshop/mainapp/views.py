# from django.shortcuts import render

# Create your views here.
import random

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from mainapp.models import Product, ProductsCategory


def index(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:3]
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None):
    links_menu = ProductsCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'Все',
                'pk': 0
            }
        else:
            category_item = get_object_or_404(ProductsCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'category': category_item,
            'products': products_list
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = random.sample(list(Product.objects.all()), 1)[0]

    context = {
        'links_menu': links_menu,
        'title': 'Продукты',
        'hot_product': hot_product
    }
    return render(request, 'mainapp/products.html', context=context)
