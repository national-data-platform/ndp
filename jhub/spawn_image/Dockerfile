FROM quay.io/jupyter/base-notebook:latest

# Install all needed packages
RUN conda install -y gcc gxx_linux-64
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy starter notebooks, Python files, etc
COPY --chown=jovyan ./starter_content/ ./work/
