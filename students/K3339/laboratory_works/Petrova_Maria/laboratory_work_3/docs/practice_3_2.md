# Практическая работа 3.2 — DRF

Отдельный проект `practice_3_2/` использует SQLite и четыре модели:

| Модель | Поля и связи |
| --- | --- |
| Profession | title, description |
| Skill | title |
| Warrior | race (student/developer/teamlead), name, level, profession, skill |
| SkillOfWarrior | warrior, skill, level освоения навыка |

Profession → Warrior — OneToMany, удаление профессии оставляет NULL.
Warrior ↔ Skill — ManyToMany через SkillOfWarrior; удаление воина или навыка
удаляет его промежуточные записи. `Profession.warriors`, `Skill.warriors`
и `warrior.warrior_skills` — заданные related_name.

## Сериализаторы и эндпоинты

Все сериализаторы — ModelSerializer. WarriorProfessionSerializer вкладывает
ProfessionSerializer; WarriorSkillsSerializer читает `warrior_skills` через source
и вкладывает SkillOfWarriorSerializer с SkillSerializer. WarriorDetailSerializer
показывает обе связи. WarriorUpdateSerializer принимает профессию по ID или null.
Навыки во вложенном ответе доступны для чтения.

| Метод | URL | Представление |
| --- | --- | --- |
| GET | `/api/skills/` | APIView, список |
| POST | `/api/skills/create/` | APIView, создание навыка |
| GET | `/api/warriors/professions/` | ListAPIView |
| GET | `/api/warriors/skills/` | ListAPIView |
| GET | `/api/warriors/<id>/` | RetrieveAPIView |
| PUT, PATCH | `/api/warriors/<id>/update/` | UpdateAPIView |
| DELETE | `/api/warriors/<id>/delete/` | DestroyAPIView |

Пример POST `/api/skills/create/`:

```json
{"title": "Python"}
```

Ответ 201 (ID условный):

```json
{"id": 1, "title": "Python"}
```

Фрагмент вложенного списка навыков воина:

```json
{"skill": [{"id": 1, "skill": {"id": 1, "title": "Python"}, "level": 1}]}
```

Внешний id — ID промежуточной записи. PATCH передаёт изменяемые поля,
PUT — все обязательные. Чтение и изменение возвращают 200, удаление — 204,
неверные данные — 400, отсутствующий воин — 404. Создание воинов через API
не предусмотрено; используйте seed_warriors или Admin. В учебной практике
не установлены ограничения доступа гостиничного API.

## Запуск

В `practice_3_2/` создайте и активируйте собственное виртуальное окружение:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_warriors
python manage.py runserver
```

Команда seed создаёт четыре профессии, шесть навыков, пять воинов и пятнадцать
связей (три навыка на воина). Практика запускается отдельно от гостиницы.
