#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN echo
RUN echo
COPY ./app /code/app

#
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]

# docker build . -t segurvich/fake_api:0.0.1 --platform=linux/amd64 --no-cache
# docker run -d --name fake_api -p 80:80 segurvich/fake_api:0.0.1