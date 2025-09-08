# mailing/management/commands/load_groups.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Load initial groups and permissions data'

    def handle(self, *args, **options):
        try:
            call_command('loaddata', 'data_groups.json')
            self.stdout.write(
                self.style.SUCCESS('Группы и права доступа успешно загружены!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке фикстуры: {e}')
            )
