#! /usr/bin/env bash

docker-compose up -d es postgres redis minio

source venv/bin/activate

cd app

uvicorn serve:app --reload