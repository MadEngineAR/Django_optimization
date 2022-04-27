from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ModelForm, CheckboxInput

from authapp.models import User
from adminapp.validator import clean_username, clean_first_name, file_size
from mainapp.models import ProductCategories, Product


class UserAdminRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(), validators=[clean_username])
    first_name = forms.CharField(widget=forms.TextInput(), validators=[clean_first_name])
    image = forms.ImageField(widget=forms.FileInput(), required=False, validators=[file_size])

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'image', 'age')
        image = forms.ImageField(widget=forms.FileInput(), required=False, validators=[file_size])
        age = forms.IntegerField(widget=forms.NumberInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите ваше имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите вашу фамилию'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите ваш адрес эл.почты'
        self.fields['age'].widget.attrs['placeholder'] = 'Введите ваш возраст'
        self.fields['image'].widget.attrs['placeholder'] = 'Добавить фотографию'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class UserAdminProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(), validators=[clean_first_name])
    image = forms.ImageField(widget=forms.FileInput(), required=False, validators=[file_size])
    age = forms.IntegerField(widget=forms.NumberInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class ProdCatAdminCreateForm(ModelForm):

    is_active = forms.BooleanField(required=False, initial={'is_active':True})

    class Meta:
        model = ProductCategories
        fields = ('name', 'descriptions', 'is_active')

    def __init__(self, *args, **kwargs):
        super(ProdCatAdminCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Наименование категории'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Описание категории'


        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-5'


class ProdAdminCreateForm(ModelForm):

    image = forms.ImageField(widget=forms.FileInput(), required=False, validators=[file_size])
    is_active = forms.BooleanField(required=False, initial={'is_active': True})

    class Meta:
        model = Product
        fields = ('name', 'descriptions', 'image', 'price', 'quantity', 'category',  'is_active')

    def __init__(self, *args, **kwargs):
        super(ProdAdminCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['placeholder'] = 'Наименование категории'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Описание товара'
        self.fields['name'].widget.attrs['placeholder'] = 'Наименование товара'
        self.fields['price'].widget.attrs['placeholder'] = 'Цена'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Количество на складе'
        self.fields['image'].widget.attrs['placeholder'] = 'Добавить фотографию'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'
