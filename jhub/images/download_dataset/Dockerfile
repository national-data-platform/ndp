FROM quay.io/jupyter/base-notebook:latest

WORKDIR /srv/starter_content

USER root

RUN apt-get update && apt-get install -y \
    git

RUN chmod a+x /usr/bin/git

RUN chown -R jovyan /srv/starter_content/

# make sudo access without password
RUN echo 'jovyan ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Install the requests library
RUN pip install requests

# Copy the Python script into the container
#COPY download_files.py .

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# install git extension
RUN pip install --upgrade jupyterlab jupyterlab-git

COPY ndp_jupyterlab_extension-0.1.28-py3-none-any.whl .
RUN pip install ndp_jupyterlab_extension-0.1.28-py3-none-any.whl
RUN rm -rf ndp_jupyterlab_extension-0.1.28-py3-none-any.whl


USER jovyan

# Set the entrypoint script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# docker build ./jhub/images/download_dataset -f ./jhub/images/download_dataset/Dockerfile -t gitlab-registry.nrp-nautilus.io/ndp/ndp-docker-images/jhub-spawn:dataset_0.0.8 --platform=linux/amd64 --no-cache