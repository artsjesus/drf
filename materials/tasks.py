from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_info(course_id, recipients, message):
    """Отправляет сообщение пользователю об обновлении материалов курса"""

    send_mail(f'Курс {course_id} обновлен', message,
              EMAIL_HOST_USER, recipients)


@shared_task
def deactivate_user():
    """Деактивирует пользователей, которые не входили в систему более 30 дней."""
    today = timezone.now().date()
    for user in User.objects.all():
        if user.last_login and user.last_login.date() + timedelta(days=30) < today:
            user.is_active = False
            user.save()
