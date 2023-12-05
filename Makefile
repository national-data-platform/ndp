COMPOSE_FILE=docker-compose.dev.yaml

default: build-run

build:
	docker build ./jhub/spawn_image -t jhub-spawn
	docker compose -f $(COMPOSE_FILE) build

build-run:
	cp .env.example ckan-docker/.env
	docker build ./jhub/spawn_image -t jhub-spawn
	docker compose -f $(COMPOSE_FILE) up --build -d

install-ckanext-ndp:
	git -C ./src_extensions clone git@github.com:national-data-platform/ckanext-ndp.git
	docker restart ndp-ckan-1

update-ckan-config:
	docker exec -it ndp-ckan-1 /bin/bash -c "ckan config-tool /srv/app/ckan.ini ckanext.ndp.jupyterhub_endpoint=http://localhost:8000"

restart:
	docker compose -f $(COMPOSE_FILE) up -d --no-deps

clean:
	docker compose -f $(COMPOSE_FILE) down --remove-orphans

dist-clean:
	docker compose -f $(COMPOSE_FILE) down --volumes