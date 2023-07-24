from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import ProductFilter, NewsFilter
from .forms import ProductForm, NewsForm, ArticleForm
from .models import Product, News


class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
    paginate_by = 5

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.filterset = None

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'


# Добавляем новое представление для создания товаров.
class ProductCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма.
    template_name = 'product_edit.html'


class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


# Представление удаляющее товар.
class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


class NewsList(ListView):
    model = News
    ordering = '-date_published'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    page_range = 5


class NewsDetail(DetailView):
    model = News
    template_name = 'one_news.html'
    context_object_name = 'one_news'


class NewsSearch(View):
    def get(self, request):
        # Используйте класс NewsFilter для фильтрации
        news_filter = NewsFilter(request.GET, queryset=News.objects.all())
        context = {
            'news_filter': news_filter
        }
        return render(request, 'news_search.html', context)


class NewsCreate(PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('simpleapp.add_news')


    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'news'
        news.save()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    model = News
    template_name = 'news_edit.html'
    fields = ['name', 'author', 'content', 'date_published']
    success_url = reverse_lazy('news_list')
    permission_required = ('simpleapp.change_news')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('simpleapp.delete_news')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = News
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('article_list')
    permission_required = ('simpleapp.add_news')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'article'
        article.save()
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'article_edit.html'
    fields = ['name', 'author', 'content', 'date_published']
    success_url = reverse_lazy('article_list')
    login_url = reverse_lazy('login')
    permission_required = ('simpleapp.change_news')



class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    permission_required = ('simpleapp.delete_news')


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'protected_page.html'


