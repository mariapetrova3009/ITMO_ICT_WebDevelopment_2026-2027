# Практическая работа 3.1 — Django ORM

Код: `practical_works/practice_3_1.py`. Используются существующие модели
`CarOwner` (наследник AbstractUser), `Car`, `DriverLicense` и `Ownership`.
Владельцы связаны с автомобилями M:N через Ownership с датами владения.
Удостоверение связано с владельцем ForeignKey.

## Запуск

Из `practical_works/` установите его requirements в собственное окружение, примените
миграции и выполните скрипт через Django shell:

```bash
python manage.py migrate
python manage.py shell < practice_3_1.py
```

Скрипт добавляет семь учебных владельцев, шесть автомобилей, семь удостоверений
и девять периодов владения. Используются create_user, exists и get_or_create;
у найденных объектов данные не заменяются. Пароль в скрипте предназначен только
для искусственных учебных аккаунтов. Результаты запросов выводятся в консоль.

## Фильтрация и связи

```python
Car.objects.filter(brand="Toyota")
CarOwner.objects.filter(first_name="Олег")
DriverLicense.objects.get(owner_id=owner.id)
CarOwner.objects.filter(cars__color="Красный").distinct()
CarOwner.objects.filter(ownership__start_date__year=2010).distinct()
```

Двойное подчёркивание проходит по связи к полю другой модели.
`distinct()` исключает повторы владельца при нескольких совпавших автомобилях.
`select_related("owner")` загружает владельца вместе с удостоверением.
`owner.cars.all()` использует прямое поле ManyToManyField.

В автомобильных моделях явный related_name не задан. Поэтому обратный доступ
к Ownership у владельца — `owner.ownership_set.all()`, а имя обратной связи
в фильтре — `ownership`. В гостинице явные имена делают обращения понятнее:
`floor.rooms.all()` и `room.accommodations.all()`.

## Агрегация и аннотация

```python
DriverLicense.objects.aggregate(earliest_date=Min("issue_date"))
Ownership.objects.filter(car__model="Camry").aggregate(latest_date=Max("start_date"))
CarOwner.objects.annotate(car_count=Count("cars", distinct=True))
Car.objects.values("brand").annotate(car_count=Count("id"))
CarOwner.objects.order_by("driverlicense__issue_date").distinct()
```

`aggregate()` возвращает один словарь для всей выборки; `annotate()` добавляет
показатель каждой записи или группе `values()`. Последний запрос сортирует
владельцев по дате удостоверения. Скрипт создаёт aware datetime через timezone.make_aware.
