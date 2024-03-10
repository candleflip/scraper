# Web scraper by URL

### :dart: TODO
- [ ] Добавить `Makefile`
- [ ] Проверить запуск с нуля
- [ ] Добавить описание проекта в `README.md`
- [ ] Добавить описание модулей проекта в структуру в `README.md`
- [ ] Дописать тесты в `test_summaries_unit.py` 

---

### :pill: Стек

- Версия языка: [Python3.10.1](https://www.python.org/downloads/release/python-3100/)
- Web-фреймворк: [FastAPI](https://fastapi.tiangolo.com/ru/)
- База Данных: [Postgres14](https://www.postgresql.org/docs/14/index.html)
- ORM: [TortoiseORM](https://tortoise.github.io/)
- Миграции: [Aerich](https://github.com/tortoise/aerich/blob/dev/README_RU.md)
- Линтер/форматер: [ruff](https://docs.astral.sh/ruff/)
- Unit-тестирование: [Pytest](https://docs.pytest.org/en/8.0.x/index.html)
- Нагрузочное тестирование: [Locust](https://locust.io/)

---

### :file_folder: Структура

```shell
*  # <-- корень проекта
├── README.md
├── docker-compose.yml
├── Makefile
└── project/
    ├── Dockerfile
    ├── Dockerfile.prod
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── crud.py
    │   │   ├── health_check.py
    │   │   └── summaries.py
    │   ├── db.py
    │   ├── main.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── pydantic/
    │   │   └── tortoise/
    │   ├── settings.py
    │   └── summarizer.py
    ├── db/
    │   ├── Dockerfile
    │   └── create.sql
    ├── entrypoint.sh
    ├── pyproject.toml
    ├── requirements.txt
    └── tests/
        ├── __init__.py
        ├── load/
        └── unit/
```

---

### :gear: Запуск

Для консистентности работы рекомендуется запускать инструкции из папки `project/` с использованием `make` команд.

1. Поднять сервисы:

```shell
make up
```

Поднимется 2 контейнера и 1 сетевой объект:

```
 [+] Running 3/3
 ⠿ Network scraper_default  Created                                        0.1s
 ⠿ Container web-db         Started                                        0.3s
 ⠿ Container web            Started                                        0.5s

```

Документация OpenAPI доступна по пути [localhost:8005/docs](http://localhost:8005/docs).
Однако, для полноценной работы необходимо накатить первую миграцию. В противном случае ручки, взаимодействующие с 
БД, будут отдавать `500 ошибку`, так как база не инициализирована.

2. Проинициализировать БД:

```shell
make db-init 
```

---

---

### :chart_with_upwards_trend: Нагрузочное тестирование

Можно провести локально, выполнив команду:

```shell
make load-test
```

---

### :wrench: Unit-тестирование

```shell
make unit-test 
```