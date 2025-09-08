# Сервис управления рассылками

Django-приложение для управления email-рассылками, клиентами и сообщениями.

## 📋 Функциональность

### 🔐 Аутентификация и авторизация
- Регистрация новых пользователей
- Аутентификация по email
- Восстановление пароля
- Профиль пользователя с аватаром

### 📊 Основные сущности
- **Клиенты** - получатели рассылок (email, ФИО, комментарий)
- **Сообщения** - шаблоны писем (тема и тело)
- **Рассылки** - планирование отправки (время, статус, получатели)
- **Попытки рассылок** - история отправки (статус, ответ сервера)

### 👥 Права доступа
- **Обычные пользователи** - видят только свои объекты
- **Менеджеры** - видят все рассылки, могут блокировать пользователей
- **Суперпользователи** - полный доступ ко всему

### ⚡ Автоматизация
- Отправка рассылок по расписанию
- Автоматическое обновление статусов
- Логирование всех операций

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <ваш-репозиторий>
cd mailing_service
```
##  2. Создание виртуального окружения
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

## 3. Установка зависимостей
```commandline

pip install -r requirements.txt

```

## 4. Настройка окружения
#### Создайте файл .env в корне проекта:
```
# Настройки Django
SECRET_KEY=ваш-secret-key
DEBUG=True

# База данных PostgreSQL
DB_NAME=mailing_db
DB_USER=postgres
DB_PASSWORD=ваш-пароль
DB_HOST=localhost
DB_PORT=5432

# Настройки почты (Mail.ru)
EMAIL_HOST_USER=ваш-email@mail.ru
EMAIL_HOST_PASSWORD=пароль-приложения

# Дополнительные настройки
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 5. Настройка базы данных

```
python manage.py migrate
python manage.py createsuperuser
```
## 6. Запуск сервера
```commandline
python manage.py runserver
```
#### Приложение будет доступно по адресу: http://127.0.0.1:8000

## 📧 Настройка почты
## Для Mail.ru
1. Включите двухфакторную авторизацию

2. Создайте пароль для приложения

3. спользуйте настройки:

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
## Тестовая отправка
```
python manage.py send_mailings
```
## 👥 Создание групп пользователей
### Создание менеджера
```
python manage.py create_managers
```
## Или через админку
1. Зайдите в /admin/

2. Создайте группу "Менеджеры"

3. Назначьте права:

- mailing.view_all_mailings

- mailing.disable_mailing

- mailing.view_all_clients

- mailing.block_client

- mailing.view_all_message

## Настройка групп

Для загрузки групп и прав доступа выполните:

```bash
python manage.py load_groups
```
Группа "Менеджеры" будет создана с правами:

- Просмотр всех рассылок

- Просмотр всех клиентов

- Просмотр всех сообщений

- Блокировка клиентов

- Отключение рассылок


## ✅ **Проверка:**

```bash
# Проверьте что фикстура загружается
python manage.py load_groups

# Проверьте что группа создалась
python manage.py shell
>>> from django.contrib.auth.models import Group
>>> Group.objects.all()
```

## 🎯 API endpoints

- / - главная страница со статистикой

- /clients/ - управление клиентами

- /messages/ - управление сообщениями

- /mailings/ - управление рассылками

- /attempts/ - просмотр попыток отправки

- /users/login/ - вход

- /users/register/ - регистрация

- /users/profile/ - профиль пользователя

## 🛠️ Технологии

- Python 3.8+

- Django 5.2

- PostgreSQL - база данных

- Redis - кэширование

- Bootstrap 5 - интерфейс

- Mail.ru SMTP - отправка почты

## 📦 Зависимости
Основные зависимости см. в requirements.txt

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE)

## 👨‍💻 Разработчик
 ### Василий - tanec_991@mail.ru
