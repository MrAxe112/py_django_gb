# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

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
    context = {
        'links_menu': ProductsCategory.objects.all(),
        'title': 'Продукты'
    }
    return render(request, 'mainapp/products.html', context=context)
