#!/bin/bash

# Pull the latest changes from your desired branch
git clone https://github.com/sergeygurvich/AB_classifier
#cp -R ./jupyter-notebooks/EcoViz_AB_classifier/. ./AB_classifier/
#rm -rf ./jupyter-notebooks

# Execute the main process of the container (passed as CMD in Dockerfile or command in Docker Compose)
exec "$@"