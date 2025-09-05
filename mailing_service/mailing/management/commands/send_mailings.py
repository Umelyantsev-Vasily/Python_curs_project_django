import logging
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from ...models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Запускает все активные рассылки"

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(f"Запуск обработки рассылок в {now}")

        # Ищем рассылки для отправки: статус "started" и текущее время в интервале
        mailings_to_send = Mailing.objects.filter(
            status="started", start_time__lte=now, end_time__gte=now
        )

        if not mailings_to_send:
            self.stdout.write("Нет активных рассылок для отправки.")
            return

        total_sent = 0
        total_failed = 0

        for mailing in mailings_to_send:
            self.stdout.write(
                f'Обрабатывается рассылка #{mailing.id} "{mailing.message.subject}"'
            )

            for client in mailing.clients.all():
                try:
                    # Пытаемся отправить письмо
                    result = send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )

                    # Если send_mail не бросил исключение, считаем успехом
                    status = "success"
                    server_response = "Успешно отправлено"
                    total_sent += 1
                    self.stdout.write(f"  ✓ Письмо для {client.email} отправлено.")

                except Exception as e:
                    # Ловим любую ошибку при отправке
                    status = "failed"
                    server_response = str(e)
                    total_failed += 1
                    self.stdout.write(f"  ✗ Ошибка для {client.email}: {e}")
                    logger.error(f"Ошибка отправки письма: {e}")

                # Создаем запись о попытке
                MailingAttempt.objects.create(
                    mailing=mailing, status=status, server_response=server_response
                )

            # Проверяем, не закончилось ли время рассылки
            if mailing.end_time <= now:
                mailing.status = "completed"
                mailing.save()
                self.stdout.write(f"  Рассылка #{mailing.id} завершена (время истекло)")

        self.stdout.write(
            self.style.SUCCESS(
                f"Обработка завершена. Успешно: {total_sent}, Неудачно: {total_failed}"
            )
        )
