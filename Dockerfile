FROM python:3.9
WORKDIR /src
ENV PYTHONPATH "${PYTHONPATH}:/src/"
ENV PATH "/src/scripts:${PATH}"
COPY . /src
RUN apt-get install -y git
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN chmod +x /src/scripts/*
ENTRYPOINT ["docker-entrypoint.sh"]