#!/bin/bash

docker rmi -f k3nny/discordbot
docker build -t k3nny/discordbot .
