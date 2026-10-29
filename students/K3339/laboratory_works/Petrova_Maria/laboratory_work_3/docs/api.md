# CRUD API гостиницы

Префикс `/api/`. Все маршруты требуют активного пользователя `is_staff=True`
с сессией Django или токеном DRF. Обычный пользователь и анонимный запрос получают 403.
Пагинация не включена, списки возвращаются массивами.

| Ресурс | Список | Объект `<id>/` |
| --- | --- | --- |
| room-types/ | GET, POST | GET, PUT, PATCH, DELETE |
| floors/ | GET, POST | GET, PUT, PATCH, DELETE |
| rooms/ | GET, POST | GET, PUT, PATCH, DELETE |
| guests/ | GET, POST | GET, PUT, PATCH, DELETE |
| employees/ | GET, POST | GET, PUT, PATCH, DELETE |
| accommodations/ | GET | GET |
| stays/ | GET | GET |
| cleaning-schedules/ | GET, POST | GET, PATCH, DELETE |

Стандартные HEAD и OPTIONS также поддерживаются. Удаление используемого объекта
даёт 400 с объяснением, неизвестный ID — 404, некорректные данные — 400,
неподдерживаемый метод после проверки доступа — 405.
Создание возвращает 201, чтение и изменение — 200, удаление — 204 без JSON.

Accommodation и Stay доступны только для чтения: запись выполняется операциями
[заселения и выселения](business_logic.md). `Employee.floors` только для чтения.
У номера с историей нельзя менять этаж и тип, у используемого типа — вместимость.
Текущую цену типа менять можно. PATCH dismissed_on сотрудника выполняет бизнес-операцию увольнения.

## Примеры

Заголовок для запросов с токеном администратора:

```http
Authorization: Token <токен_администратора>
Content-Type: application/json
```

POST `/api/room-types/`:

```json
{"name": "Двухместный", "capacity": 2, "price_per_night": "5000.00"}
```

Ответ 201:

```json
{"id": 1, "name": "Двухместный", "capacity": 2, "price_per_night": "5000.00"}
```

POST `/api/floors/`: `{"number": 1}`. POST `/api/rooms/`:

```json
{"number": "101", "floor": 1, "room_type": 1, "phone": "101"}
```

Ответ включает id и переданные поля. PATCH `/api/rooms/1/` с `{"phone": "102"}`
обновляет телефон. ID во всех примерах условные — используйте существующие записи.

## Вложенная сериализация

GET `/api/rooms/1/accommodations/` показывает поля номера и список Accommodation
в `accommodations` (OneToMany):

```json
{"id": 1, "number": "101", "floor": 1, "room_type": 1, "phone": "101", "accommodations": []}
```

GET `/api/employees/1/schedule/` показывает поля сотрудника, список ID этажей `floors`
и `schedule` — список назначений с вложенным объектом этажа:

```json
{"id": 1, "first_name": "Анна", "last_name": "Тестовая", "middle_name": "", "hired_on": "2026-01-01", "dismissed_on": null, "user": null, "floors": [1], "schedule": [{"id": 1, "employee": 1, "floor": {"id": 1, "number": 1}, "weekday": 0, "valid_from": "2026-01-01", "valid_to": null}]}
```

Это ManyToMany через CleaningSchedule. Несколько назначений на один этаж могут
дать повторяющиеся ID в `floors`. Явные вложенные ModelSerializer используют
related_name и source, без depth. Основные CRUD используют Generic API Views.
