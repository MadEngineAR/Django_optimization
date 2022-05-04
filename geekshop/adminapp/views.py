import itertools
import random

from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProdCatAdminCreateForm, ProdAdminCreateForm
from authapp.models import User
from django.contrib.auth.decorators import user_passes_test

from adminapp.mixin import BaseClassContextMixin, CustomDispatchMixin
from mainapp.models import Product, ProductCategories
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem

# @user_passes_test(lambda u: u.is_superuser)
# def index(request):
#     return render(request, 'adminapp/admin.html')

from ordersapp.views import OrderUpdate


class IndexTemplateView(TemplateView, BaseClassContextMixin, CustomDispatchMixin):
    title = 'Главная страница'
    template_name = 'adminapp/admin.html'


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     content = {
#         'title': 'Администратор | Пользователи',
#         'users': User.objects.all()
#     }
#     return render(request, 'adminapp/admin-users-read.html', content)


class UserListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    title = 'Администратор | Пользователи'
    template_name = 'adminapp/admin-users-read.html'
    context_object_name = 'users'


# @user_passes_test(lambda u: u.is_superuser)
# def admin_user_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:admin_users'))
#
#         else:
#             print(form.errors)
#     else:
#         form = UserAdminRegisterForm()
#     content = {'title': 'Администратор | Создание профиля',
#                'form': form}
#     return render(request, 'adminapp/admin-users-create.html', content)


class UserCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    title = 'Администратор | Создание профиля'
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('adminapp:admin_users')

    def post(self, request, *args, **kwargs):  # передача сообщения
        messages.success(request, 'Вы успешно создали пользователя')
        return super().post(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_user_update(request, id):
#     user_select = User.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(instance=user_select, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно изменили свои данные')
#             return HttpResponseRedirect(reverse('adminapp:admin_users'))
#         else:
#             print(form.errors)
#     else:
#         form = UserAdminProfileForm(instance=user_select)
#     content = {'title': 'Администратор | Редактирование профиля',
#                'form': form,
#                'user_select': user_select}
#     return render(request, 'adminapp/admin-users-update-delete.html', content)


class UserUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    title = 'Администратор | Редактирование профиля'
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    def post(self, request, *args, **kwargs):  # передача сообщения
        messages.success(request, 'Вы успешно изменили свои данные')
        return super().post(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_user_delete(request, id):
#     user_select = User.objects.get(id=id).delete()
#     # user_select.is_active = False
#     # user_select.save()
#     return HttpResponseRedirect(reverse('adminapp:admin_users'))


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    def post(self, request, *args, **kwargs):  # передача сообщения
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories(request):
#     content = {'title': 'Geekshop | Категории товаров',
#                'categories': ProductCategories.objects.all()
#                }
#     return render(request, 'adminapp/admin_product_categories_read.html', content)


class ProdCatListView(ListView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategories
    title = 'Администратор | Категории товаров'
    template_name = 'adminapp/admin_product_categories_read.html'
    context_object_name = 'categories'


# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories_create(request):
#     if request.method == 'POST':
#         form = ProdCatAdminCreateForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:admin_product_categories'))
#
#         else:
#             print(form.errors)
#     else:
#         form = ProdCatAdminCreateForm()
#     content = {'title': 'Администратор | Создание категорий продуктов',
#                'form': form}
#     return render(request, 'adminapp/admin_product_categories_create.html', content)


class ProdCatCreateView(CreateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategories
    title = 'Администратор | Создание категорий продуктов'
    template_name = 'adminapp/admin_product_categories_create.html'
    form_class = ProdCatAdminCreateForm
    success_url = reverse_lazy('adminapp:admin_product_categories')

    def post(self, request, *args, **kwargs):  # передача сообщения
        messages.success(request, 'Вы успешно создали категорию пользователя')
        return super().post(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories_update(request, id):
#     prod_cat_select = ProductCategories.objects.get(id=id)
#     if request.method == 'POST':
#         form = ProdCatAdminCreateForm(instance=prod_cat_select, data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно изменили категорию')
#             return HttpResponseRedirect(reverse('adminapp:admin_product_categories'))
#         else:
#             print(form.errors)
#     else:
#         form = ProdCatAdminCreateForm(instance=prod_cat_select)
#     content = {'title': 'Администратор | Редактирование категории товаров',
#                'form': form,
#                'prod_cat_select': prod_cat_select}
#     return render(request, 'adminapp/admin_product_categories_update_delete.html', content)


class ProdCatUpdateView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = ProductCategories
    title = 'Администратор | Редактирование категории товаров'
    template_name = 'adminapp/admin_product_categories_update_delete.html'
    form_class = ProdCatAdminCreateForm
    success_url = reverse_lazy('adminapp:admin_product_categories')

    def post(self, request, *args, **kwargs):  # передача сообщения
        messages.success(request, 'Вы успешно изменили категорию товаров')
        return super().post(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories_delete(request, id):
#     prod_cat_select = ProductCategories.objects.get(id=id)
#     prod_cat_select.is_active = False
#     prod_cat_select.save()
#     return HttpResponseRedirect(reverse('adminapp:admin_product_categories'))


class ProdCatDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategories
    template_name = 'adminapp/admin_product_categories_update_delete.html'
    form_class = ProdCatAdminCreateForm
    success_url = reverse_lazy('adminapp:admin_product_categories')

    def post(self, request, *args, **kwargs):  # передача сообщения
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    content = {'title': 'Geekshop | Товары',
               'products': Product.objects.all()
               }
    return render(request, 'adminapp/admin_products_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_create(request):
    if request.method == 'POST':
        form = ProdAdminCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_products'))

        else:
            print(form.errors)
    else:
        form = ProdAdminCreateForm()
    content = {'title': 'Администратор | Создание продукта',
               'form': form}
    return render(request, 'adminapp/admin_products_create.html', content)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_update(request, id):
    prod_select = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProdAdminCreateForm(instance=prod_select, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно изменили продукт')
            return HttpResponseRedirect(reverse('adminapp:admin_products'))
        else:
            print(form.errors)
    else:
        form = ProdAdminCreateForm(instance=prod_select)
    content = {'title': 'Администратор | Редактирование товара',
               'form': form,
               'prod_select': prod_select}
    return render(request, 'adminapp/admin_products_update_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_delete(request, id):
    prod_select = Product.objects.get(id=id).delete()
    # # prod_cut_select.is_active = False
    # # prod_cut_select   .save()
    return HttpResponseRedirect(reverse('adminapp:admin_products'))


class OrderAdminList(ListView, BaseClassContextMixin):
    model = Order
    title = 'Geekshop|Заказы пользователя'
    template_name = 'adminapp/admin_orders_read.html'


class OrderAdminUpdate(UpdateView, BaseClassContextMixin):
    model = Order
    fields = []
    title = 'Geekshop|Администратор редактирование заказа'
    success_url = reverse_lazy('adminapp:admin_orders')

    def get_context_data(self, **kwargs):
        context = super(OrderAdminUpdate, self).get_context_data()
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)

            for num, form in enumerate(formset.forms):
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderAdminUpdate, self).form_valid(form)


def get_next_order_status():

    status_tuple = (Order.FORMING, Order.SEND_TO_PROCESSED, Order.PAID, Order.PROCESSED, Order.READY, Order.CANCEL)
    for status in itertools.cycle(status_tuple):
        yield status


gen = get_next_order_status()

# Смена статуса происходит случайно. Коряво конечно, но генератор не срабатывает и по другому не получилось
def admin_orders_change_status(request, id):
    order = Order.objects.get(pk=id)
    status_tuple = (Order.FORMING, Order.SEND_TO_PROCESSED, Order.PAID, Order.PROCESSED, Order.READY, Order.CANCEL)
    # gen = get_next_order_status()
    # order.status = next(gen)
    order.status = next(gen)
    order.save()
    return HttpResponseRedirect(reverse('adminapp:admin_orders'))
