# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django
from mainapp.models import Product, ProductsCategory
from mainapp.services import get_hot_product, get_same_products, get_links_menu, get_product, get_products


def index(request):
    context = {
        'title': 'Главная',
        'products': get_products()[:3]
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None, page=1):
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

        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': get_links_menu(),
            'title': 'Продукты',
            'category': category_item,
            'products': products_paginator
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': get_links_menu(),
        'title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', context=context)


def product_details(request, pk):
    title = 'продукты'
    context = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_product(pk)
    }

    return render(request, 'mainapp/product_details.html', context=context)
