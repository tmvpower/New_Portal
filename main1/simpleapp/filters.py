from django_filters import FilterSet
from .models import Product, News


class ProductFilter(FilterSet):
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Product
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'name': ['icontains'],
           # количество товаров должно быть больше или равно
           'quantity': ['gt'],
           'price': [
               'lt',  # цена должна быть меньше или равна указанной
               'gt',  # цена должна быть больше или равна указанной
           ],
       }

class NewsSearch(FilterSet):
    class Meta:
        model = News
        fields = {
            'name': ['icontains'],
            'autor': ['icontains'],
            'date_published': ['gt'],
        }

    @classmethod
    def as_view(cls):
        pass