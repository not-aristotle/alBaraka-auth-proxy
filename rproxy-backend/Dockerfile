FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    apt-utils \
    gcc \
    musl-dev \
    postgresql-server-dev-12 \
    python3.8 \
    python3.8-dev \
    python3-pip \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN update-alternatives --force --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --force --set  python3 /usr/bin/python3.8

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod +x /app/gunicorn.sh && \
    chmod +x /app/celery-worker.sh && \
    chmod +x /app/celery-beat.sh && \
    chmod +x /app/wait-for-it.sh