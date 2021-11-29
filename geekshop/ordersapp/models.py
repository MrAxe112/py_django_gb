from django.db import models
from django.conf import settings
from mainapp.models import Product


class Order (models.Model):
    STATUS_FORMING = 'FM'
    STATUS_SENT_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_DONE = 'DN'
    STATUS_CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (STATUS_FORMING, 'формируется'),
        (STATUS_SENT_TO_PROCEED, 'отправлен в обработку'),
        (STATUS_PAID, 'оплачен'),
        (STATUS_PROCEEDED, 'Обрабатывается'),
        (STATUS_DONE, 'Готов к выдаче'),
        (STATUS_CANCEL, 'Отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, default=STATUS_FORMING, max_length=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_product_type_quantity(self):
        _items = self.orderitems.select_related()
        return len(_items)

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, _items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity
