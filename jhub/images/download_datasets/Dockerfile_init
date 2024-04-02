FROM python:3.9-slim

# Install the requests library
RUN pip install requests

# Copy the Python script into the container
COPY download_files.py /download_files.py

# You can set a default value for the environment variable if you like
ENV DATASET_ID=default-value

# Set the command to run the script
CMD ["python", "/download_files.py"]