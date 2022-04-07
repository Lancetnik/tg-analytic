#! /usr/bin/env bash
set -e

python elastic_mapping.py
python minio_mapping.py
python init_db.py