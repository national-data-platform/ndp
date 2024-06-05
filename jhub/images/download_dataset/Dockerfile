FROM quay.io/jupyter/base-notebook:latest

WORKDIR /srv/starter_content/Dataset_Resources

USER root

RUN apt-get update && apt-get install -y \
    git

RUN chmod a+x /usr/bin/git

#RUN git clone https://github.com/national-data-platform/jupyter-notebooks
#
#RUN pip install -r /srv/jupyter-notebooks/minimal_starter_content/requirements.txt

# RUN mkdir /srv/starter_content/

#RUN cp -R /srv/jupyter-notebooks/minimal_starter_content/. /srv/starter_content/

RUN chown -R jovyan /srv/starter_content/

# make sudo access without password
RUN echo 'jovyan ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Install the requests library
RUN pip install requests

# Copy the Python script into the container
COPY download_files.py .

# You can set a default value for the environment variable if you like
# ENV DATASET_ID=default-value

# Set the command to run the script
# CMD python download_files.py && rm -rf download_files.py

# USER jovyan


# Copy the entrypoint script into the container
RUN echo
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

USER jovyan

# Set the entrypoint script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# docker build ./jhub/images/download_dataset -f ./jhub/images/download_dataset/Dockerfile -t gitlab-registry.nrp-nautilus.io/ndp/ndp-docker-images/jhub-spawn:dataset_0.0.1 --platform=linux/amd64 --no-cache