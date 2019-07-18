FROM ubuntu:14.04
FROM python:3

RUN apt-get update
RUN apt-get -y install alsa-utils

ENV XDG_RUNTIME_DIR="D:\Github_stock\test_dockerize_python_app\tmp"

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5432
RUN sleep(3000)
CMD ["python", app.py"]