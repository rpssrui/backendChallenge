PYTHON ?= python3

start:
	$(PYTHON) manage.py runserver

test:
	$(PYTHON) manage.py test backendChallenge

migrate:
	$(PYTHON) manage.py migrate

makemigrations:
	$(PYTHON) manage.py makemigrations

bootstrap:
	make migrate
	make makemigrations
	make start

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} +

docker-build:
	docker-compose build

docker-migrate:
	docker-compose run web python manage.py migrate

docker-run:
	docker-compose up -d
	make docker-migrate
	docker-compose logs -f web

docker-stop:
	docker-compose down

help:
	@echo "Available commands:"
	@echo "  start            - Start the Django development server"
	@echo "  test             - Run tests"
	@echo "  migrate          - Apply database migrations"
	@echo "  makemigrations   - Create new database migrations"
	@echo "  clean            - Clean up __pycache__ and .pyc files"
	@echo "  bootstrap        - Run migrate, makemigrations and start in sequence"
	@echo "  docker-build     - Build Docker containers"
	@echo "  docker-run       - Run Docker containers with migrations"
	@echo "  docker-stop      - Stop Docker containers"
	@echo "  help             - Show this help message"
