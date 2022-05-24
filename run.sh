#!/bin/bash

docker-compose build --build-arg UID=$(id -u) web
docker-compose build nginx
docker-compose up -d