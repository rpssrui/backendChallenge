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

help:
	@echo "Available commands:"
	@echo "  start            - Start the Django development server"
	@echo "  test             - Run tests"
	@echo "  migrate          - Apply database migrations"
	@echo "  makemigrations   - Create new database migrations"
	@echo "  clean            - Clean up __pycache__ and .pyc files"
	@echo "  help             - Show this help message"
