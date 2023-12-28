#!/usr/bin/env bash
./stopandremove.sh
docker compose up --build --force-recreate --no-deps -d

