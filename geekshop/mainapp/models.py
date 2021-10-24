from django.db import models

# Create your models here.


class ProductsCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="название")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('-id',)


class Product(models.Model):
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="название")
    image = models.ImageField(upload_to='products', blank=True, verbose_name='изображение')
    short_desc = models.CharField(max_length=255, verbose_name='краткое описание')
    description = models.TextField(verbose_name='полное описание')
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
