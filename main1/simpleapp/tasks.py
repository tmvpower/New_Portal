# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import News, Category


@shared_task
def send_weekly_newsletter():
    # Определяем даты начала и конца недели
    today = timezone.now()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=7)

    # Получаем последние новости за неделю
    latest_news = News.objects.filter(date_published__gte=start_of_week, date_published__lt=end_of_week)

    # Генерируем содержание письма с последними новостями
    email_subject = "Еженедельная рассылка новостей"
    email_message = "Последние новости:\n\n"

    for news in latest_news:
        email_message += f"{news.title}\n"
        email_message += f"{news.content}\n\n"

    # Отправляем письмо подписчикам
    subscribers = Category.subscribers.objects.all()
    for subscriber in subscribers:
        send_mail(email_subject, email_message, 'TMV@example.com', [subscriber.email])
