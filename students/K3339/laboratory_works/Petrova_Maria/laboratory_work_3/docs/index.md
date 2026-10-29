# Лабораторная работа №3

Тема: «Реализация серверной части приложения средствами Django и Django REST Framework».
Вариант №1 — «Администратор гостиницы».

Цель — создать серверное API управления номерным фондом, гостями, заселениями,
сотрудниками и уборкой, закрепить ORM, связи моделей и сериализацию, реализовать
аналитику, квартальный отчёт и авторизацию.

## Технологии и структура

- Django 5.2: модели, ORM, миграции, транзакции, административная панель и сессии.
- Django REST Framework 3.16: ModelSerializer, Serializer, Generic API Views и APIView.
- PostgreSQL и psycopg 3: основная база гостиницы.
- Djoser 2.3 и стандартный DRF TokenAuthentication: регистрация и токены.
- python-dotenv: параметры локального окружения.
- MkDocs 1.6: эта документация.

`practical_works/` содержит практику ORM 3.1 и ранее созданные учебные модели автомобилей.
`practice_3_2/` — отдельный проект воинов. `hotel_api/` — основная лабораторная.
Каждый Django-проект запускается отдельно. Главная база гостиницы — PostgreSQL;
практические проекты используют свои настройки и SQLite.

## Установка гостиницы

Из папки `laboratory_work_3`:

```bash
cd hotel_api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

При первом запуске, если `.env` ещё отсутствует, скопируйте `.env.example` в `.env`.
Существующий `.env` сохраняйте. Укажите реквизиты своей PostgreSQL: `DB_NAME`, `DB_USER`,
`DB_PASSWORD`, `DB_HOST`, `DB_PORT`. Для существующего Docker-контейнера запустите
Docker Desktop и сам контейнер; используйте его опубликованный порт. Compose-файл
в лабораторной не поставляется, новая база автоматически не создаётся.

При отдельной установке PostgreSQL администратор создаёт роль и базу, если их ещё нет:

```sql
CREATE ROLE hotel_user LOGIN;
\password hotel_user
CREATE DATABASE hotel_db OWNER hotel_user;
```

`\password` запрашивает пароль интерактивно. Не меняйте пароли существующих ролей.

Дополнительно `.env` поддерживает `SECRET_KEY` и `DEBUG`. По умолчанию включён DEBUG
и используется учебный локальный ключ, чтобы сохранить прежний запуск. Для внешнего
размещения задайте собственный секрет и `DEBUG=False`; текущие ALLOWED_HOSTS разрешают
только localhost и 127.0.0.1. Реальные секреты не включайте в Git.

```bash
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`migrate` также создаёт стандартную таблицу токенов DRF. Структура восьми моделей
гостиницы не менялась. Существующие миграции сохранены.

Откройте `/api-auth/login/` для входа администратора в браузере, `/api/rooms/`
для API или `/admin/` для административной панели. Корневой `/` не имеет страницы.
Регистрация через Djoser описана в [разделе авторизации](authentication.md).

## Основные команды

| Команда из hotel_api | Назначение |
| --- | --- |
| `python manage.py check` | Проверка конфигурации |
| `python manage.py makemigrations --check --dry-run` | Поиск незаписанных изменений моделей |
| `python manage.py showmigrations` | Состояние миграций |
| `python manage.py migrate` | Применение миграций |
| `python manage.py createsuperuser` | Создание администратора |
| `python manage.py seed_hotel` | Необязательные искусственные справочники |
| `python manage.py runserver` | Локальный сервер |

`seed_hotel` создаёт типы, этажи, номера DEMO-1..3, двух гостей и двух сотрудников.
Он не создаёт аккаунты, заселения и уборки; повторный запуск не перезаписывает найденные записи.
Не запускайте его, если демонстрационные данные не нужны.

## Документация

Из `laboratory_work_3`, после установки requirements гостиницы:

```bash
hotel_api/.venv/bin/python -m mkdocs serve
hotel_api/.venv/bin/python -m mkdocs build --strict
```

Локальная документация доступна на http://127.0.0.1:8000; при одновременно работающем
Django выберите `mkdocs serve -a 127.0.0.1:8001`. Сборка помещается в `site/`, исключённый из Git.
