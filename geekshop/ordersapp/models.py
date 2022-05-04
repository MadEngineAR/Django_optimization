from django.conf import settings
from django.db import models


# Create your models here.
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCESSED = 'STP'
    PAID = 'PD'
    PROCESSED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Формируется'),
        (SEND_TO_PROCESSED, 'Отправлен в обработку'),
        (PAID, 'Оплачен'),
        (PROCESSED, 'Обрабатывается'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменен')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создан', auto_now=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now_add=True)
    paid = models.DateTimeField(verbose_name='Оплачен', null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='Статус заказа', max_length=5, default=FORMING)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity



