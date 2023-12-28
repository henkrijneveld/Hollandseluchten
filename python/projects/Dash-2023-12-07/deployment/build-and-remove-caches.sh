#!/usr/bin/env bash
./stopandremove.sh
docker compose build --no-cache
./start.sh
