from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives, mail_admins
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
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

@login_required
def send_weekly_newsletter():
    # Отправляем рассылку только тем пользователям, которые подписаны на какие-либо категории
    subscribed_users = User.objects.filter(category__isnull=False).distinct()

    # Получаем текущую дату и дату недели назад
    today = datetime.today().date()
    one_week_ago = today - timedelta(weeks=1)

    for user in subscribed_users:
        # Получаем все статьи, добавленные за последнюю неделю в разделах, на которые подписан пользователь
        new_articles = News.objects.filter(author__category__subscribers=user, date_published__date__gte=one_week_ago)

        # Формируем содержание письма
        message = ''
        for article in new_articles:
            message += f'{article.title}: {article.content[:50]}\n'

        # Отправляем письмо пользователю с новыми статьями
        send_mail(
            'Weekly Newsletter',
            message,
            'noreply@yourdomain.com',  # Укажите здесь ваш адрес электронной почты
            [user.email],
            fail_silently=False,
        )
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



def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            # Отправляем обновление всем подписчикам данной категории
            news.send_update_email()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'create_news.html', {'form': form})


@login_required
def subscribe_category(request, category_id):
    category = get_object_or_404('Category', pk=category_id)
    user = request.user

    if user in category.subscribers.all():
        category.subscribers.remove(user)
    else:
        category.subscribers.add(user)

    return redirect('category_news', category_id=category_id)

def create_news(request):
    if request.method == 'POST':
        user = request.user
        # Проверяем, сколько новостей уже опубликовано пользователем за сутки
        news_count_today = News.objects.filter(author=user, date_published__date=datetime.today()).count()
        if news_count_today >= 3:
            return render(request, 'error.html', {'message': 'You have reached the limit of news publications for today.'})

        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()

            # Отправляем уведомления подписчикам категории
            subscribers = news.category.subscribers.all()
            for subscriber in subscribers:
                mail_admins(
                    subject=f'New article in {news.category.name}',
                    message=f'{news.title}: {news.content[:50]}',
                    recipient_list=[subscriber.email],
                )

            return redirect('news_detail', pk=news.pk)

    else:
        form = NewsForm()

    return render(request, 'create_news.html', {'form': form})

