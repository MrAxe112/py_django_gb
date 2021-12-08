import hashlib
import pytz
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from authapp.models import ShopUser
from django.conf import settings
from authapp.models import ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form.control'
            field.help_text = ""


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form.control'
            field.help_text = ""

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Регистрация возможна только для пользователей старше 18 лет.")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 4:
            raise forms.ValidationError("Имя пользователя должно быть не менее 5 символов")
        return data

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activate_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()

        return user


class ShopUserChangeForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ""
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Регистрация возможна только для пользователей старше 18 лет.")
        return data


class ShopUserProfileEditForm(forms.ModelForm):

    class Meta:
        model = ShopUserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ""