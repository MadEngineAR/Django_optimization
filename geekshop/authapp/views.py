from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, FormView, LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from django.urls import reverse, reverse_lazy

from authapp.mixin import BaseClassContextMixin
from authapp.models import User
from basket.models import Basket


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#
#     content = {'title': 'Geekshop | Авторизация',
#                'form': form}
#     return render(request, 'authapp/login.html', content)


class LoginFormView(LoginView, BaseClassContextMixin):
    title = 'Geekshop | Авторизация'
    template_name = 'authapp/login.html'
    form_class = UserLoginForm


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем! Вы зарегистрированы')
#             return HttpResponseRedirect(reverse('authapp:login'))
#
#         else:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#     content = {'title': 'Geekshop | Регистрация',
#                'form': form}
#     return render(request, 'authapp/register.html', content)


class RegisterFormView(FormView, BaseClassContextMixin):
    model = User
    title = 'Geekshop | Регистрация'
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):  # передача сообщения
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verification_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Поздравляем! Вы зарегистрированы')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                print(form.errors)
        else:
            print(form.errors)
            # messages.set_level(request, messages.ERROR)
            # messages.error(request, form.errors, extra_tags='register')
        content = {'form': form}
        return render(request, 'authapp/register.html', content)

    def send_verification_link(self, user):
        verification_link = reverse('authapp:verification', args=[user.email, user.activation_key])
        subject = f'Для активации пользователя {user.username} пройдите по ссылке'
        message = f'Для активации пользователя {user.username} на портале \n {settings.DOMAIN_NAME}{verification_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verification(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
                return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))
# @login_required
# def profile(request):
#     user_select = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно изменили свои данные')
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=user_select)
#     content = {'title': 'Geekshop | Профиль',
#                'form': form,
#                'baskets': Basket.objects.filter(user=user_select)}
#     return render(request, 'authapp/profile.html', content)


class ProfileFormView(UpdateView, BaseClassContextMixin):
    title = 'Geekshop | Профиль'
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    # extra_context = {'baskets': Basket.objects.filter(user=?????}

    def post(self, request, *args, **kwargs):  # передача сообщения
        # messages.success(request, 'Вы успешно изменили свои данные', extra_tags='profile')
        # # content = {'title': 'Geekshop | Профиль',
        # #                'form': form,
        # #                'baskets': Basket.objects.filter(user=self.get_object())}
        # # return render(request, 'authapp/profile.html', content)
        # return super().post(request, *args, **kwargs)
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):  #
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно изменили свои данные', extra_tags='profile')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.pk)

# def logout(request):
#     auth.logout(request)
#     return render(request, 'mainapp/index.html')


class Logout(LogoutView):
    template_name = 'mainapp/index.html'
