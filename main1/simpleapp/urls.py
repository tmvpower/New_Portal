from django.urls import path
from .views import ProductsList, ProductDetail, NewsList, NewsDetail, ProductCreate, ProductUpdate, ProductDelete, \
   NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete, ProtectedView, NewsSearch

urlpatterns = [
   path('', ProductsList.as_view(), name='product_list'),
   path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('protected/', ProtectedView.as_view(), name='protected_view'),
]
