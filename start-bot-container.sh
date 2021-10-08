#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0))

if [ ! -d ./data ]; then
    mkdir ${THIS_DIR}/data
fi

docker rm -f discordbot
docker run -it -v ${THIS_DIR}/src/:/bot -d k3nny/discordbot python main.py
