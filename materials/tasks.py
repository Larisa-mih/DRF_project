from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
import pytz

from django.conf import settings
from config.settings import EMAIL_HOST_USER

from materials.models import Subscription, Course
from users.models import User


@shared_task
def send_email(course_id):
    """Отправляет письмо подписчикам при обновлении курса"""
    course = Course.objects.get(pk=course_id)
    subscribers = course.subscription.all()
    sub_email_list = []
    for subscriber in subscribers:
        sub_email_list.append(subscriber.user)
    message = f'Курс "{course.name}" обновлен'

    send_mail(
        subject="Информирование об обновлении курса",
        message=f"Здравствуйте!\n"
                f"{message}",
        from_email=EMAIL_HOST_USER,
        recipient_list=sub_email_list
    )


@shared_task
def check_user():
    """Деактивирует пользователей, если не были онлайн более 30 дней"""
    active_users = User.objects.filter(is_active=True)
    zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(zone)
    for user in active_users:
        if user.last_login:
            if now - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()
                print(f"Пользователь {user} заблокирован за пассивность")
