from django.urls import path

from .filters import NewsSearch
# Импортируем созданное нами представление
from .views import ProductsList, ProductDetail, NewsList, NewsDetail, ProductCreate, ProductUpdate, ProductDelete, \
   NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('product/', ProductsList.as_view(), name='product_list'),
   path('product/<int:pk>', ProductDetail.as_view(), name='product_detail'),
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('product/create/', ProductCreate.as_view(), name='product_create'),
   path('product/<int:pk>/update', ProductUpdate.as_view(), name='product_update'),
   path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('news/search', NewsSearch.as_view(), name='news_search'),
   # Страница создания новости
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   # Страница редактирования новости
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   # Страница удаления новости
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   # Страница создания статьи
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   # Страница редактирования статьи
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   # Страница удаления статьи
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]