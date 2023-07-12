from django.urls import path
# Импортируем созданное нами представление
from .views import ProductsList, ProductDetail, NewsList, NewsDetail

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('products/', ProductsList.as_view()),
   path('<int:pk>', ProductDetail.as_view()),
   path('news/', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view()),
]