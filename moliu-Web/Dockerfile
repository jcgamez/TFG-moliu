# Instructions for creating moliuWeb image

FROM python:3.10-slim

# Interpreter doesn’t generate .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Send python output straight to the terminal(standard output) without being buffered
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev libmagic1 ffmpeg openjdk-11-jre wget unzip\
    && rm -rf /var/lib/apt/lists/*

RUN wget https://prdownloads.sourceforge.net/weka/weka-3-8-6.zip \
    && unzip weka-3-8-6.zip

ENV CLASSPATH=/weka-3-8-6/weka.jar

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

ARG UID=1000

# Build argument UID: Create a user with host machine user UID, otherwise use 1000.
RUN useradd -u ${UID} -U moliu

WORKDIR /app
RUN chown -R moliu:moliu /app

USER moliu:moliu
COPY --chown=moliu:moliu . .

# Create media folder for uploaded files
# and static folder for production files
RUN mkdir media static

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]