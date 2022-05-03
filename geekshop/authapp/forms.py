import hashlib
import random

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from authapp.models import User, UserProfile
from authapp.validator import clean_username, clean_first_name, file_size


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(), validators=[clean_username])

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(), validators=[clean_username])
    first_name = forms.CharField(widget=forms.TextInput(), validators=[clean_first_name])

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите ваше имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите вашу фамилию'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите ваш адрес эл.почты'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user

    # def clean_first_name(self):
    #     first_name = self.cleaned_data['first_name']
    #     if re.search('[a-zA-Z0-9]', self.cleaned_data['first_name']):
    #         raise ValidationError("Пожалуйста введите ваше имя на кириллице. Не используйте цифры без цифр")
    #     return first_name
    #
    # def clean_username(self):
    #     if not re.match('[a-zA-Z]', self.cleaned_data['username']):
    #         raise ValidationError("Пожалуйста введите имя пользователя латинскими буквами")
    #
    #     return self.cleaned_data['username']


class UserProfileForm(UserChangeForm):

    first_name = forms.CharField(widget=forms.TextInput(), validators=[clean_first_name])
    image = forms.ImageField(widget=forms.FileInput(), required=False, validators=[file_size])
    age = forms.IntegerField(widget=forms.NumberInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class UserProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'gender':
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'



