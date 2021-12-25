from django.db import models
from django.conf import settings
from mainapp.models import Product


class OrderQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            for item in object.orderitems.select_related():
                item.product.quantity += item.quantity
                item.product.save()
            object.is_active = False
            object.save()
        super().delete(*args, **kwargs)


class Order (models.Model):
    objects = OrderQuerySet.as_manager()

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

    def delete(self, *args, **kwargs):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
