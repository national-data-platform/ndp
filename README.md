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
- Ckan: data catalog service
- JupyterHub: notebook service
- MLflow: AI/ML experimentation tracker service
- NDP Frontend: frontend service

## Git submodules
The following git submodules are used:
- [MLflow](https://github.com/national-data-platform/mlflow)
- [CKAN](https://github.com/national-data-platform/ckan-docker)
- [NDP Frontend](https://github.com/national-data-platform/ndp-frontend)

The Dockerspawer version of Jupyterhub provided in this [repo](https://github.com/national-data-platform/jupyterhub-deploy-docker) is used as a starting point/inspiration.

Other dependencies:
- Mlflow Keycloak Plugin through [ndp auth plugin](https://github.com/national-data-platform/ndp_mlflow_auth)
- Python scripts to pre-load ckan and setup the ckan harvester [ckan-data-loader](https://github.com/national-data-platform/ckan-data-loader)


## Docker-compose
With the git submodules we can use docker compose extension functionality to easily
use the docker-compose manifest file from each repo and make necessary changes in the current docker-compose file.

First, make a copy of the `.env.example`:
```
cp .env.example .env
```

Note that will need some .env so please contact the NDP Admins.

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

## Development mode (default)
In development mode, ckan extensions can be downloaded to [src_extensions](/src_extensions)
and some commands are provided through the Makefile.


The rest of the instructions are meant to setup two ckan extensions; [ckanext-ndp](https://github.com/national-data-platform/ckanext-ndp) and [ckanext-keycloak](https://github.com/national-data-platform/ckanext-keycloak).

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

After this change you will need to restart ckan to pick up the new changes.

### CKAN NDP Extension
Install [ndp ckan keycloak extension](https://github.com/national-data-platform/ckanext-ndp):
```
make download-ckanext-keycloak
```

Next, append `keycloak` to the ckan plugin environment variable `CKAN__PLUGINS`.

### Remarks
1. There are cases when ckan doesn't pick up some environment variables from the .env file so sometimes its better to mount a copy of the ckan.ini file. There is a comment in the docker-compose file for this in this [line](/docker-compose.dev.yaml?plain=24). I have noticed that it sometimes doesn't pick up `CKAN___ROOT__PATH` which is needed for the nginx reverse proxy to work.

## Production mode

For now, the development docker-compose file is used for production mode with some minor adjustments (the nginx config file and docker-compose file).

Both [ckanext-ndp](https://github.com/national-data-platform/ckanext-ndp) and [ckanext-keycloak](https://github.com/national-data-platform/ckanext-keycloak) are built in the ckan production [Dockerfile](/ckan-docker/ckan/Dockerfile).

Some remarks in the development section also apply to production. 
