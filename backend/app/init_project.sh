#! /usr/bin/env bash
set -e

source ../venv/bin/activate

python elastic_mapping.py
python minio_mapping.py
python init_db.py