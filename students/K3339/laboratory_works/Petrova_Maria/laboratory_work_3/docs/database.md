# Модель данных гостиницы

Восемь моделей описаны в `hotel_api/hotel_app/models.py`. Все имеют первичный ключ id.
Деньги представлены DecimalField, даты — DateField.

| Модель | Основные поля | Назначение |
| --- | --- | --- |
| RoomType | name, capacity, price_per_night | Тип, вместимость 1–3, текущий тариф за номер |
| Floor | number | Уникальный положительный номер этажа |
| Room | number, floor, room_type, phone | Уникальный номер комнаты, этаж и тип |
| Guest | last_name, first_name, middle_name, passport_series, passport_number, arrival_city | Гость, уникальная пара серии и номера паспорта |
| Accommodation | room, check_in, planned_check_out, actual_check_out, price_per_night | Оплачиваемый период номера, сохранённый тариф |
| Stay | guest, accommodation | Уникальная пара гость–заселение |
| Employee | last_name, first_name, middle_name, hired_on, dismissed_on, user, floors | Сотрудник, необязательный аккаунт, этажи |
| CleaningSchedule | employee, floor, weekday, valid_from, valid_to | Назначение уборки с периодом действия |

`actual_check_out`, `dismissed_on`, `valid_to` допускают NULL. Отчество можно оставить пустым.
`Employee.user` — необязательная OneToOne со стандартным User Django; удаление User
оставляет NULL. Клиенту Guest аккаунт не нужен. Регистрация User не создаёт Employee.

## Связи

- Floor → Room и RoomType → Room: OneToMany, обратное имя `rooms`.
- Room → Accommodation: OneToMany, `accommodations`.
- Guest → Stay и Accommodation → Stay: OneToMany, `stays`.
- Employee ↔ Floor: ManyToMany, `Employee.floors` с `through=CleaningSchedule`,
  обратное имя `employees`; записи назначений доступны через `cleaning_assignments` с обеих сторон.
- Guest и Accommodation логически связаны M:N через Stay, но отдельное поле
  ManyToManyField для этой связи в моделях не объявлено.

## История и ограничения

Все гостиничные ForeignKey используют PROTECT: удаление используемого справочника
не удалит историю. Исключение — Employee.user с SET_NULL.
База проверяет положительные цены, вместимость 1–3, корректность порядка дат,
уникальность паспортов, номеров и связей. Бизнес-проверки пересечения и вместимости
выполняются через API в транзакциях.

Accommodation представляет один заезд группы. Несколько Stay у одной Accommodation
не увеличивают цену. При заселении копируется текущий RoomType.price_per_night;
позднейшее изменение цены типа не меняет историю. bulk_create не вызывает save(),
поэтому при прямом использовании ORM снимок цены нужно задавать явно.

Общие даты у всей группы; индивидуальных дат Stay нет. Город в Guest хранит
актуальное значение, история городов не ведётся. CleaningSchedule хранит назначения,
а не подтверждения выполненной уборки. Повторный найм сотрудника не моделируется.
