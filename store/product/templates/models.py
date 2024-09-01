from django.db import models

from users.models import User


# Create your models here.

class ProductsCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название", unique=True)
    description = models.TextField(max_length=300, verbose_name="Описание", null=True, blank=True)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"Категории {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название товара")
    description = models.TextField(max_length=450, verbose_name="Описание товара")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', null=True)
    category = models.ForeignKey(ProductsCategory, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"Товар {self.name} {self.category}"


class BasketQuerySet(models.QuerySet):  # я расширил метод QuerySet данным классом (довольно таки мощная штука)
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(verbose_name="Корзина пользователя", to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity
