from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategories, Product

admin.site.register(ProductCategories)


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'descriptions', ('price', 'quantity'), 'category')
    readonly_fields = ('descriptions',)
    ordering = ('name', 'price')
    search_fields = ('name',)
