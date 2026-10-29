# Djoser и авторизация

Используются стандартный Django User, Djoser и rest_framework.authtoken.
Собственная модель пользователей и JWT не подключены. Djoser устанавливает
SimpleJWT как транзитивную зависимость, но его маршруты в проекте не включены.
Стандартные маршруты Djoser подключены через include; собственные ViewSet и Router
для гостиницы не используются.

## Регистрация

```http
POST /auth/users/
Content-Type: application/json

{"username": "student", "email": "student@example.com", "password": "Study-secret-Q7!x"}
```

Ответ 201:

```json
{"id": 1, "username": "student", "email": "student@example.com"}
```

Пароль проходит стандартные валидаторы Django и хранится в виде хеша, в ответ
не включается. Повторный username или слабый пароль дают 400. Подтверждение почты
не требуется. Новый User имеет is_staff=False и is_superuser=False.
Поля привилегий не входят в сериализаторы Djoser: передача is_staff, is_superuser,
groups, user_permissions при регистрации или PATCH своего профиля не даёт прав.

## Получение токена

```http
POST /auth/token/login/
Content-Type: application/json

{"username": "student", "password": "Study-secret-Q7!x"}
```

Ответ 200:

```json
{"auth_token": "<выданный_токен>"}
```

Неправильный пароль или неактивный пользователь дают 400. Токен секретный:
не публикуйте его и передавайте по HTTPS при внешнем размещении.

## Текущий пользователь

```http
GET /auth/users/me/
Authorization: Token <выданный_токен>
```

Ответ 200:

```json
{"id": 1, "username": "student", "email": "student@example.com"}
```

Доступны стандартные безопасные поля Djoser. HIDE_USERS скрывает чужие профили
от обычных пользователей. Без действующей авторизации запрос отклоняется.

## Выход

```http
POST /auth/token/logout/
Authorization: Token <выданный_токен>
```

Ответ 204 без тела. Токен удаляется, повторный запрос с ним отклоняется.
Для следующего входа получите новый токен. Выход по токену не завершает
независимую браузерную сессию Django; для неё используйте `/api-auth/logout/`.

## Права и браузер

| Действие | Анонимный | Обычный User | is_staff=True |
| --- | --- | --- | --- |
| Регистрация, получение токена | Да | Да | Да |
| Свои данные, выход по токену | Нет | Да | Да |
| CRUD гостиницы, гости и паспорта | Нет | Нет | Да |
| Заселение, выселение, сотрудники, уборка | Нет | Нет | Да |
| Аналитика и квартальный отчёт | Нет | Нет | Да |
| Django Admin | Нет | Нет | По стандартным модельным разрешениям; записи истории только просмотр |

В DEFAULT_AUTHENTICATION_CLASSES сначала SessionAuthentication, затем
TokenAuthentication; DEFAULT_PERMISSION_CLASSES — IsAdminUser для гостиницы.
Djoser задаёт собственные стандартные permissions регистрации и профиля.
Порядок сохраняет прежние ответы 403 при отсутствии/ошибке авторизации.
Действительный токен обычного пользователя также даёт 403 для гостиницы.

`/api-auth/login/` и сессии `/admin/` сохранены. CSRF middleware включён,
SessionAuthentication требует CSRF для POST/PUT/PATCH/DELETE.
При действующей браузерной сессии она проверяется первой, поэтому добавленный
Authorization не отменяет её CSRF-проверку. Для curl с токеном не передавайте
браузерные cookies.

Административные права выдаёт доверенный администратор Django, регистрация их
не выдаёт. После повышения is_staff обычный токен пользователя также сможет
обращаться к гостиничному API: permissions проверяют текущее состояние User.

Официальные материалы: [Djoser: подключение](https://djoser.readthedocs.io/en/stable/getting_started.html),
[токенные эндпоинты](https://djoser.readthedocs.io/en/latest/token_endpoints.html).
