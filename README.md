# Web scraper by URL

### :pill: Стек

- Версия языка: [Python3.10](https://www.python.org/downloads/release/python-3100/)
- Web-фреймворк: [FastAPI](https://fastapi.tiangolo.com/ru/)
- ORM: [TortoiseORM](https://tortoise.github.io/)
- Миграции: [Aerich](https://github.com/tortoise/aerich/blob/dev/README_RU.md)
- Unit-тестирование: [Pytest](https://docs.pytest.org/en/8.0.x/index.html)
- Линтер/форматер: [ruff](https://docs.astral.sh/ruff/)
- Нагрузочное тестирование: [Locust](https://locust.io/)


### :bookmark_tabs: Структура

```
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
│   │   ├── pydantic.py
│   │   └── tortoise.py
│   ├── settings.py
│   └── summarizer.py
├── db/
│   ├── Dockerfile
│   └── create.sql
├── entrypoint.sh
├── htmlcov/
├── migrations/
│   └── models/
├── pyproject.toml
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── load/
    │   ├── __init__.py
    │   └── dev.py
    └── unit/
        ├── __init__.py
        ├── conftest.py
        ├── test_health_check.py
        ├── test_summaries.py
        └── test_summaries_unit.py
```


### Запуск

Для консистентности работы рекомендуется запускать инструкции из корня проекта.

1. Поднять сервисы:

```shell
docker-compose up --detach --build
```

Поднимется 2 контейнера и 1 сетевой объект:

```
[+] Running 3/3
 ⠿ Network fastapi-tdd-docker_default     Created                                                                                                                    0.0s
 ⠿ Container fastapi-tdd-docker-web-db-1  Started                                                                                                                    0.3s
 ⠿ Container fastapi-tdd-docker-web-1     Started
```

Документация OpenAPI доступна по пути [localhost:8005/docs](http://localhost:8005/docs).
Однако, для полноценной работы необходимо накатить первую миграцию. В противном случае ручки, взаимодействующие с 
БД, будут отдавать `500 ошибку`.

2. Накатить первую миграцию на создание структуры БД:

```shell
docker-compose exec web aerich upgrade 
```