up:
	docker-compose up --detach --build

db-init:
	docker-compose exec web aerich init-db

db-upgrade:
	docker-compose exec web aerich upgrade

load-test:
	locust -f tests/load/dev.py

unit-test:
	docker-compose exec web python -m pytest -xlvvs --cov="."
