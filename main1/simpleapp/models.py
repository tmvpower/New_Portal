from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True, # названия товаров не должны повторяться
    )
    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
    )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products', # все продукты в категории будут доступны через поле products
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class News(models.Model):
    name = models.CharField(max_length=50, unique=True)
    text = models.TextField()
    date_published = models.DateTimeField(default=datetime.now)
    autor = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name} {self.text}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


