FROM python:3.9-slim-buster
WORKDIR /src
ENV PYTHONPATH "${PYTHONPATH}:/src/"
COPY . /src
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN python -m pip install --upgrade pip