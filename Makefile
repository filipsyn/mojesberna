reset: down up

install: env venv up migrate

on: up dev

up:
	docker-compose up -d

down:
	docker-compose down

env:
	export FLASK_APP='src/app.py'
	cp .example.env .env

venv:
	python -m venv venv
	source venv/bin/activate
	pip install -r src/requirements.txt

migrate:
	flask db migrate
	flask db upgrade

dev:
	export FLASK_APP='src/app.py'
	flask run --host 0.0.0. --port 8080
