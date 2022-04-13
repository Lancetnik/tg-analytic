#! /usr/bin/env bash

docker-compose up -d postgres

source venv/bin/activate

cd app

uvicorn serve:app --port 8003