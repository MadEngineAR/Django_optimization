from django.urls import path
from adminapp.views import admin_products, admin_products_create, \
    admin_products_update, \
    admin_products_delete, IndexTemplateView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
    ProdCatListView, ProdCatCreateView, ProdCatUpdateView, ProdCatDeleteView

app_name = 'adminapp'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('user-create/', UserCreateView.as_view(), name='admin_user_create'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='admin_user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_user_delete'),
    path('product-categories/', ProdCatListView.as_view(), name='admin_product_categories'),
    path('product-categories-create/', ProdCatCreateView.as_view(), name='admin_product_categories_create'),
    path('product-categories-update/<int:pk>/', ProdCatUpdateView.as_view(),
         name='admin_product_categories_update'),
    path('product-categories-delete/<int:pk>/', ProdCatDeleteView.as_view(),
         name='admin_product_categories_delete'),
    path('product/', admin_products, name='admin_products'),
    path('product-create/', admin_products_create, name='admin_products_create'),
    path('product-update/<int:id>/', admin_products_update, name='admin_products_update'),
    path('product-delete/<int:id>/', admin_products_delete, name='admin_products_delete')
]
