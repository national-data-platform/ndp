# NDP

The National Data Platform (NDP) is a federated and extensible data ecosystem to promote
collaboration, innovation and equitable use of data on top of existing cyberinfrastructure capabilities.

The National Data Platform was funded by [NSF 2333609](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2333609) under CI, CISE Research Resources programs. Any opinions, findings, conclusions, or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the funders.

## Git clone

NDP uses git submodules so cloning must be done through the following command:
```
git clone --recurse-submodules git@github.com:national-data-platform/ndp.git
```

In the case the submodules are not present you can also init them with the following command:
```
git submodule update --init
```

## Services
NDP consist of the following core services:
- CKAN and CKAN2: two identical, but separate and isolated data catalog services
- NDP JupyterHub: notebook service running on NRP k8s cluster (Nautilus)
- MLflow: AI/ML experimentation tracker service
- NDP Frontend: frontend service
- NDP API: backend service containing endpoints for managing workspaces, token and other endpoints for future functionalities
- Keycloak: authentication and authorization

## Git submodules
The following git submodules are used:
- [MLflow](https://github.com/national-data-platform/mlflow)
- [CKAN](https://github.com/national-data-platform/ckan-docker)
- [NDP Frontend](https://github.com/national-data-platform/ndp-frontend)
- [NDP API](https://github.com/national-data-platform/ndp-workspaces-api)

Other dependencies:
- CKAN NDP Plugin through [ndp plugin](https://github.com/national-data-platform/ckanext-ndp) (_note: this might be deprecated / not needed_)
- CKAN / CKAN2 Keycloak Plugin through [ndp ckan keycloak plugin](https://github.com/national-data-platform/ckanext-keycloak) (_note: this might be deprecated / not needed_)
- CKAN2 Catalog Additions Plugin through [ndp catalog additions plugin](https://github.com/national-data-platform/ckanext-ndpcatalogadditions)
- Mlflow Keycloak Plugin through [ndp auth plugin](https://github.com/national-data-platform/ndp_mlflow_auth)
- Python scripts to pre-load ckan and setup the ckan harvester [ckan-data-loader](https://github.com/national-data-platform/ckan-data-loader)

#### NDP JupyterHub:
- The Dockerspawer version of Jupyterhub provided in this [repo](https://github.com/national-data-platform/jupyterhub-deploy-docker) is used as a starting point/inspiration (local).
- NDP Jupyterhub Helm chart deployment and image files are located in this [repo](https://github.com/national-data-platform/ndp-jupyterhub) 

#### Keycloak:
- [NDP Keycloak AAI](https://github.com/national-data-platform/ndp-keycloak-aai)

## Docker-compose
With the git submodules we can use docker compose extension functionality to easily
use the docker-compose manifest file from each repo and make necessary changes in the current docker-compose file.

First, make a copy of the `.env.example`, `.env_ckan2.example`, `ckan.ini.example`, `ckan2.ini.example`:
```
cp .env.example .env
cp .env_ckan2.example .env_ckan2
cp ckan.ini.example ckan.ini
cp ckan2.ini.example ckan2.ini
```

Note that will need modification of environment variables, depending on your environment setup, so please contact the NDP Admins.

* The development docker-compose file is `docker-compose.dev.yaml`.
* The production docker-compose file is `docker-compose.prod.yaml`.

The following command builds and runs the containers:
```
make
```

Cleanup:
```
make clean
```

Cleanup and delete volumes:
```
make dist-clean
```

Useful commands examples directly via Docker CLI:
```
# Start all services
docker compose -f docker-compose.dev.yaml up --build -d

# Start one service
docker compose -f docker-compose.dev.yaml up frontend --build -d

# List containers
docker ps

# Watch logs
docker logs ndp-frontend-1 -f

# Remove one service
docker compose -f docker-compose.dev.yaml down frontend

# Remove one service
docker compose -f docker-compose.dev.yaml down frontend

# Remove all services
docker compose -f docker-compose.dev.yaml down

# Remove all services and volumes
docker compose -f docker-compose.dev.yaml down -v

# Remove all services and orphans even if they don't appear in the current file
docker compose -f docker-compose.dev.yaml down --remove-orphans
```

## Development mode (default)
In development mode, ckan extensions can be downloaded to [src_extensions](/src_extensions)
and some commands are provided through the Makefile.


The rest of the instructions are meant to setup three ckan extensions; [ckanext-ndp](https://github.com/national-data-platform/ckanext-ndp), [ckanext-keycloak](https://github.com/national-data-platform/ckanext-keycloak), and [ckanext-ndpcatalogadditions](https://github.com/national-data-platform/ckanext-ndpcatalogadditions) 

### CKAN NDP Extension
Install [ndp ckan extension](https://github.com/national-data-platform/ckanext-ndp):
```
make download-ckanext-ndp
```

Next, append `ndp` to the ckan plugin environment variable `CKAN__PLUGINS`.

Update ckan config to add Jupyterhub endpoint:
```
make update-ckan-config
```

_Note:
To avoid the issue from the remarks, we can mount ckan.ini file directly to the container. Therefore, the extension might be needed to be inserted under plugins section into
`ckan.plugins` variable._

After this change you will need to restart ckan to pick up the new changes.

### CKAN Keycloak Extension
Install [ndp ckan keycloak extension](https://github.com/national-data-platform/ckanext-keycloak):
```
make download-ckanext-keycloak
```
Next, append `keycloak` to the ckan plugin environment variable `CKAN__PLUGINS`.

_Note:
To avoid the issue from the remarks, we can mount ckan.ini file directly to the container. Therefore, the extension might be needed to be inserted under plugins section into
`ckan.plugins` variable._

After this change you will need to restart ckan to pick up the new changes.

### CKAN2 NDPCatalogAdditions Extension
Install [ckanext-ndpcatalogadditions](https://github.com/national-data-platform/ckanext-ndpcatalogadditions):
```
make download-ckanext-ndpcatalogadditions
```

Next, append `ndpcatalogadditions` to the ckan plugin environment variable `CKAN__PLUGINS` in `.env_ckan2` file.

_Note:
To avoid the issue from the remarks, we can mount ckan2.ini file directly to the container. Therefore, the extension might be needed to be inserted under plugins section into
`ckan.plugins` variable._

After this change you will need to restart ckan to pick up the new changes.

### Remarks
1. There are cases when ckan doesn't pick up some environment variables from the .env file so sometimes its better to mount a copy of the ckan.ini file. There is a comment in the docker-compose file for this in this [line](/docker-compose.dev.yaml?plain=24). I have noticed that it sometimes doesn't pick up `CKAN___ROOT__PATH` which is needed for the nginx reverse proxy to work.
2. Same issue, as #1. There are cases when ckan2 doesn't pick up some environment variables from the .env_ckan2 file so sometimes its better to mount a copy of the ckan2.ini file.

## Production mode
The production docker-compose file is docker-compose.prod.yaml.

```
docker compose -f docker-compose.prod.yaml up --build -d
```

Look for additional helpful Docker CLI commands in the Development section. 

- Both [ckanext-ndp](https://github.com/national-data-platform/ckanext-ndp) and [ckanext-keycloak](https://github.com/national-data-platform/ckanext-keycloak) are built in the ckan production [Dockerfile](/ckan-docker/ckan/Dockerfile).
- [ckanext-ndpcatalogadditions](https://github.com/national-data-platform/ckanext-ndp) plugin is built in CKAN2 production [Dockerfile2](/ckan-docker/ckan/Dockerfile2).

Some remarks in the development section also apply to production. 

## Environments:
#### TEST
https://github.com/national-data-platform/ndp/tree/ndp-test-environment  
For testing and development.

#### STAGING
https://github.com/national-data-platform/ndp/tree/ndp-staging-environment  
For testing and demos. Pre-production environment.

#### PROD
Production, user-facing environment.
