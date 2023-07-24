from datetime import datetime

from django.contrib.auth.models import User
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
        return f'{self.name}: {self.description[:20]}'


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class News(models.Model):
    objects = None
    name = models.CharField(max_length=50, unique=True)
    text = models.TextField()
    date_published = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return f'{self.name} {self.text}'

    @property
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.comment_set = None
        self.post_set = None


    def update_rating(self):
        post_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_rating = self.comment_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_post_rating = self.post_set.aggregate(models.Sum('comment__rating'))['comment__rating__sum'] or 0

        self.rating = (post_rating * 3) + comment_rating + comment_post_rating
        self.save()


class Post(models.Model):
    type_choices = [('news', 'News'), ('post', 'Post')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=type_choices)
    created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_length = 124
        if len(self.text) <= preview_length:
            return self.text
        else:
            return self.text[:preview_length] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
