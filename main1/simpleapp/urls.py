from django.urls import path
from .views import ProductsList, ProductDetail, NewsList, NewsDetail, ProductCreate, ProductUpdate, ProductDelete, \
   NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete, ProtectedView, NewsSearch

urlpatterns = [
   path('products/', ProductsList.as_view(), name='product_list'),
   path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('products/create/', ProductCreate.as_view(), name='product_create'),
   path('products/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('products/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('news/search/', NewsSearch.as_view(), name='news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('protected/', ProtectedView.as_view(), name='protected_view'),
]
