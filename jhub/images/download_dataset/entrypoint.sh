#!/bin/bash

#python download_files.py
#rm -rf download_files.py

mkdir -p /srv/starter_content/_User-Persistent-Storage_/GIT
git config --global credential.helper "store --file=/srv/starter_content/_User-Persistent-Storage_/GIT/.git-credentials"

# Execute the main process of the container (passed as CMD in Dockerfile or command in Docker Compose)
exec "$@"