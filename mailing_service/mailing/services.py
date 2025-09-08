# mailing/services.py
from django.core.mail import send_mail
from django.conf import settings
from .models import MailingAttempt


def send_mailing(mailing):
    """Функция отправки рассылки для каждого клиента"""
    for client in mailing.clients.all():
        try:
            # Отправляем письмо
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = "success"
            server_response = "Успешно отправлено"
        except Exception as e:
            status = "failed"
            server_response = str(e)

        # Создаем запись о попытке
        MailingAttempt.objects.create(
            mailing=mailing,
            client=client,  # ← добавляем клиента
            status=status,
            server_response=server_response
        )
