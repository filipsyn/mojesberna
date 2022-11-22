reset: down up

install: down env up

up:
	docker-compose up -d

down:
	docker-compose down

env:
	cp container.example.env container.env
	cp .example.env .env

shell:
	docker exec -it mojesberna-webapp sh
