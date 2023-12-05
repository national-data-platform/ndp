COMPOSE_FILE=docker-compose.dev.yaml

default: build-run

build:
	docker build ./jhub/spawn_image -t jhub-spawn
	docker compose -f $(COMPOSE_FILE) build

build-run:
	cp .env.example ckan-docker/.env
	docker build ./jhub/spawn_image -t jhub-spawn
	docker compose -f $(COMPOSE_FILE) up --build -d

restart:
	docker compose -f $(COMPOSE_FILE) up -d --no-deps

clean:
	docker compose -f $(COMPOSE_FILE) down --remove-orphans

dist-clean:
	docker compose -f $(COMPOSE_FILE) down --volumes