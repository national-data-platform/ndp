COMPOSE_FILE=docker-compose.dev.yaml

default: build-run

build:
	docker build ./jhub/spawn_image -f ./jhub/spawn_image/Dockerfile_pgml -t jhub-spawn --no-cache
	docker compose -f $(COMPOSE_FILE) build

build-run:
	docker build ./jhub/spawn_image -f ./jhub/spawn_image/Dockerfile_pgml -t jhub-spawn --no-cache
	docker compose -f $(COMPOSE_FILE) up --build -d

download-ckanext-ndp:
	git -C ./src_extensions clone git@github.com:national-data-platform/ckanext-ndp.git

download-ckanext-keycloak:
	git -C ./src_extensions clone git@github.com:national-data-platform/ckanext-keycloak.git --branch ndp

update-ckan-config:
	docker compose -f $(COMPOSE_FILE) exec -it ckan /bin/bash -c "ckan config-tool /srv/app/ckan.ini ckanext.ndp.jupyterhub_endpoint=http://localhost:8000"

restart:
	docker compose -f $(COMPOSE_FILE) up -d --no-deps

clean:
	docker compose -f $(COMPOSE_FILE) down --remove-orphans

dist-clean:
	docker compose -f $(COMPOSE_FILE) down --volumes

ckan-clean:
	docker exec ndp-ckan-1 sh -c "yes | ckan -c ckan.ini db clean && ckan -c ckan.ini db init"
	docker restart ndp-ckan-1
