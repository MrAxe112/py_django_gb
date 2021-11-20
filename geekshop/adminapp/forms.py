from authapp.forms import ShopUserRegisterForm, ShopUserChangeForm
from authapp.models import ShopUser
from mainapp.models import ProductsCategory, Product
from django import forms


class ShopUserAdminRegisterForm(ShopUserRegisterForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ShopUserAdminChangeForm(ShopUserChangeForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductsCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

