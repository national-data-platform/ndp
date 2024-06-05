#!/bin/bash

python download_files.py
rm -rf download_files.py

# Execute the main process of the container (passed as CMD in Dockerfile or command in Docker Compose)
exec "$@"