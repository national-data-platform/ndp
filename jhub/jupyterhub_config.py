# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os
from oauthenticator.generic import GenericOAuthenticator

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = int(os.environ.get("JUPYTERHUB_PORT", 8080))


# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator
c.GenericOAuthenticator.client_id = os.environ.get("JUPYTERHUB_KEYCLOAK_CLIENT_ID")
c.GenericOAuthenticator.client_secret = os.environ.get("JUPYTERHUB_KEYCLOAK_CLIENT_SECRET")
c.GenericOAuthenticator.token_url = os.environ.get("OAUTH2_TOKEN_URL")
c.GenericOAuthenticator.userdata_url = os.environ.get("KEYCLOAK_USERDATA_URL")
c.GenericOAuthenticator.userdata_params = {'state': 'state'}
c.GenericOAuthenticator.username_key = 'preferred_username'
c.GenericOAuthenticator.login_service = 'Keycloak'
c.GenericOAuthenticator.scope = ['openid', 'profile']
c.GenericOAuthenticator.allow_all = True
c.Authenticator.auto_login = True
# c.Authenticator.add_user_cmd = ['adduser', '-q', '--gecos', '""', '--disabled-password', '--force-badname']
# c.Authenticator.blacklist = set()
# c.Authenticator.whitelist = set()

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]

# Pass environment variables for MLFlow connection
c.DockerSpawner.environment = {
    'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
    'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
    'MLFLOW_TRACKING_URI': os.environ.get('MLFLOW_TRACKING_URI'),
    'MLFLOW_S3_ENDPOINT_URL': os.environ.get('MLFLOW_S3_ENDPOINT_URL'),
    'AWS_BUCKET_NAME': os.environ.get('AWS_BUCKET_NAME'),
}
