#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r render_requirements.txt

python manage.py migrate