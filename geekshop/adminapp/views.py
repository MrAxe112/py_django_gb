from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from authapp.models import ShopUser
from mainapp.models import Product, ProductsCategory
from adminapp.forms import ShopUserAdminChangeForm, ShopUserAdminRegisterForm, ProductCategoryEditForm


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserAdminRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users_list'))
    else:
        user_form = ShopUserAdminRegisterForm()

    context = {
        'form': user_form
    }

    return render(request, 'adminapp/user_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', 'username')

    context = {
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminChangeForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users_list'))
    else:
        user_form = ShopUserAdminChangeForm(instance=current_user)

    context = {
        'form': user_form
    }

    return render(request, 'adminapp/user_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users_list'))
    context = {
        'object': current_user
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    category_list = ProductsCategory.objects.all().order_by('-is_active')

    context = {
        'category_list': category_list
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        categories_form = ProductCategoryEditForm(request.POST, request.FILES)

        if categories_form.is_valid():
            categories_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        categories_form = ProductCategoryEditForm()

    context = {
        'form': categories_form
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    current_category = get_object_or_404(ProductsCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=current_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        category_form = ProductCategoryEditForm(instance=current_category)

    context = {
        'form': category_form
    }

    return render(request, 'adminapp/category_form.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    current_category = get_object_or_404(ProductsCategory, pk=pk)

    if request.method == "POST":
        if current_category.is_active:
            current_category.is_active = False
        else:
            current_category.is_active = True
        current_category.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))
    context = {
        'object': current_category
    }
    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_list(request, pk):
    context = {
        'category': get_object_or_404(ProductsCategory, pk=pk),
        'objects': Product.objects.filter(category__pk=pk).order_by('-is_active')
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    context = {

    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    context = {

    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    context = {

    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    context = {

    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_details(request, pk):
    context = {

    }
    return render(request, 'adminapp/users.html', context)
