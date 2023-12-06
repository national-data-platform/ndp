# NDP

The National Data Platform (NDP) is a federated and extensible data ecosystem to promote
collaboration, innovation and equitable use of data on top of existing cyberinfrastructure capabilities.

The National Data Platform was funded by [NSF 2333609](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2333609) under CI, CISE Research Resources programs. Any opinions, findings, conclusions, or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the funders.

## Services
NDP consist of the following core services:
- Ckan: data catalog service
- JupyterHub: notebook service
- MLflow: AI/ML experimetation tracker service

## Git submodules
The following git submodules are used:
- [MLflow](https://github.com/national-data-platform/mlflow)
- [CKAN](https://github.com/national-data-platform/ckan-docker)

The Dockerspawer version of Jupyterhub provided in this [repo](https://github.com/national-data-platform/jupyterhub-deploy-docker) is used as a starting point/inspiration.

## Docker-compose
With the git submodules we can use docker compose extension functionality to easily
use the docker-compose manifest file from each repo and make necessary changes in the current docker-compose file.

First, make a copy of the `.env.example`:
```
cp .env.example .env
```

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

## CKAN NDP Extension
Install [ndp ckan extension](https://github.com/national-data-platform/ckanext-ndp):
```
make download-ckanext-ndp
```

Install extension and update ckan config to add Jupyterhub endpoint:
```
make update-ckan-config
```
