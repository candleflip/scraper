up:
	docker-compose up --detach --build

init:
	docker-compose exec web aerich init-db

migrate:
	docker-compose exec web aerich upgrade

load_test:
	locust -f tests/load/dev.py

unit_test:
	docker-compose exec web python -m pytest -xlvvs --cov="."
