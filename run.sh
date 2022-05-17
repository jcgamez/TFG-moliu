#!/bin/bash

docker-compose build --build-arg UID=$(id -u) web
docker-compose up -d