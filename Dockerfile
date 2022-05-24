FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev libmagic1 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

ARG UID=1000

RUN useradd -u ${UID} -U moliu

WORKDIR /app
RUN chown -R moliu:moliu /app

USER moliu:moliu
COPY --chown=moliu:moliu . .
RUN mkdir media static

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]