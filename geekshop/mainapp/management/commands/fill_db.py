import json
from abc import ABC

from django.core.management.base import BaseCommand
from mainapp.models import Product, ProductCategories

from authapp.models import User


def load_from_json(some_file):
    with open(some_file, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(username='MadEngine', email='1@vk.ru', password='1')
        categories = load_from_json('mainapp/fixtures/cat.json')
        ProductCategories.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductCategories(**cat)
            new_category.save()

        products = load_from_json('mainapp/fixtures/prod.json')
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = ProductCategories.objects.get(id=category)
            prod['category'] = _category
            new_category = Product(**prod)
            new_category.save()

