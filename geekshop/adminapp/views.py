from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from authapp.models import ShopUser
from mainapp.models import Product, ProductsCategory
from adminapp.forms import ShopUserAdminChangeForm, ShopUserAdminRegisterForm, ProductCategoryEditForm, ProductEditForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.utils.decorators import method_decorator


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(AccessMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminRegisterForm
    success_url = reverse_lazy('adminapp:users')


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', 'username')

    context = {
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)
# class UserListView(AccessMixin, ListView):
#     model = ShopUser
#     template_name = 'adminapp/users.html'
#
#  Не реализован ListView: после применения на страницу не попадает цикл For in


class UserUpdateView(AccessMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminChangeForm
    success_url = reverse_lazy('adminapp:users')


class UserDeleteView(AccessMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    category_list = ProductsCategory.objects.all().order_by('-is_active')

    context = {
        'category_list': category_list
    }
    return render(request, 'adminapp/categories.html', context)
# class CategoriesListView(AccessMixin, ListView):
#     model = ProductsCategory
#     template_name = 'adminapp/categories.html'
#
#  Не реализован ListView: после применения на страницу не попадает цикл For in


class CategoryCreateView(AccessMixin, CreateView):
    model = ProductsCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:category_list')


class CategoryUpdateView(AccessMixin, UpdateView):
    model = ProductsCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:category_list')


class CategoryDeleteView(AccessMixin, DeleteView):
    model = ProductsCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:category_list')


@user_passes_test(lambda u: u.is_superuser)
def product_list(request, pk):
    context = {
        'category': get_object_or_404(ProductsCategory, pk=pk),
        'objects': Product.objects.filter(category__pk=pk).order_by('-is_active')
    }

    return render(request, 'adminapp/products.html', context)
# class ProductListView(AccessMixin, ListView):
#     model = Product
#     template_name = 'adminapp/products.html'
#  Не реализован ListView: после применения на страницу не попадает цикл For in


class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/products_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('adminapp:category_list', args=[self.kwargs['pk']])


class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/products_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDeleteView(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_details.html'
