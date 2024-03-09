# Web scraper by URL

### :pill: Стек

- Версия языка: [Python3.10](https://www.python.org/downloads/release/python-3100/)
- Web-фреймворк: [FastAPI](https://fastapi.tiangolo.com/ru/)
- ORM: [TortoiseORM](https://tortoise.github.io/)
- Миграции: [Aerich](https://github.com/tortoise/aerich/blob/dev/README_RU.md)
- Unit-тестирование: [Pytest](https://docs.pytest.org/en/8.0.x/index.html)
- Линтер/форматер: [ruff](https://docs.astral.sh/ruff/)
- Нагрузочное тестирование: [Locust](https://locust.io/)

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
│       └── 0_20240210201136_init.sql
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
