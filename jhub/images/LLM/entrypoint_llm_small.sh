#!/bin/bash

# Pull the latest changes from your desired branch
git clone https://github.com/national-data-platform/jupyter-notebooks
cp -R ./jupyter-notebooks/llm/NDP\ LLM\ Service/. .
rm -rf ./jupyter-notebooks

# Execute the main process of the container (passed as CMD in Dockerfile or command in Docker Compose)
exec "$@"