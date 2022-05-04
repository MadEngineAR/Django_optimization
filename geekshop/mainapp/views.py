from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from pathlib import Path

from django.views.generic import DetailView
from mainapp.models import Product, ProductCategories

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.


def index(request):
    content = {'title': 'geekshop Store'}
    return render(request, 'mainapp/index.html', content)


def products(request, id_category=None, page=1):
    if id_category:
        products_ = Product.objects.filter(category_id=id_category)
        cancel = 'Сбросить фильтр'  # необходимо для того, чтобы "Cбросить фильтр" появлялся только при
        # выборе  категории, а не на главной."
        categories = ProductCategories.objects.filter(id=id_category)   # В шаблоне отображается только одна выбранная
        # категория
    else:
        products_ = Product.objects.filter(is_active=True)  # Чтобы в пагинатор не попали неактивные продукты(удаленные)
        categories = ProductCategories.objects.all()
        cancel = None
    pagination = Paginator(products_, per_page=2)
    try:
        product_pagination = pagination.page(page)
    except PageNotAnInteger:
        product_pagination = pagination.page(1)
    except EmptyPage:
        product_pagination = pagination.page(pagination.num_pages)

    content = {'title': 'geekshop - Каталог',
               'products': product_pagination,
               'categories': categories,
               'cancel': cancel
               }
    return render(request, 'mainapp/products.html', content)


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/detail.html'
