import os
import django
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from mailing.models import Client, Message, Mailing


# Настройка Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def update_permissions():
    print("Обновление названий permissions...")

    # Обновляем permissions для Client
    client_content_type = ContentType.objects.get_for_model(Client)
    perm, created = Permission.objects.get_or_create(
        codename="view_all_clients",
        content_type=client_content_type,
        defaults={"name": "Может просматривать всех клиентов"},
    )
    if not created:
        perm.name = "Может просматривать всех клиентов"
        perm.save()
        print("✓ Обновлено: view_all_clients")

    perm, created = Permission.objects.get_or_create(
        codename="block_client",
        content_type=client_content_type,
        defaults={"name": "Может блокировать клиентов"},
    )
    if not created:
        perm.name = "Может блокировать клиентов"
        perm.save()
        print("✓ Обновлено: block_client")

    # Обновляем permissions для Message
    message_content_type = ContentType.objects.get_for_model(Message)
    perm, created = Permission.objects.get_or_create(
        codename="view_all_messages",
        content_type=message_content_type,
        defaults={"name": "Может просматривать все сообщения"},
    )
    if not created:
        perm.name = "Может просматривать все сообщения"
        perm.save()
        print("✓ Обновлено: view_all_messages")

    # Обновляем permissions для Mailing
    mailing_content_type = ContentType.objects.get_for_model(Mailing)
    perm, created = Permission.objects.get_or_create(
        codename="view_all_mailings",
        content_type=mailing_content_type,
        defaults={"name": "Может просматривать все рассылки"},
    )
    if not created:
        perm.name = "Может просматривать все рассылки"
        perm.save()
        print("✓ Обновлено: view_all_mailings")

    perm, created = Permission.objects.get_or_create(
        codename="disable_mailing",
        content_type=mailing_content_type,
        defaults={"name": "Может отключать рассылки"},
    )
    if not created:
        perm.name = "Может отключать рассылки"
        perm.save()
        print("✓ Обновлено: disable_mailing")

    print("Все названия permissions обновлены на русские! ✅")


if __name__ == "__main__":
    update_permissions()
