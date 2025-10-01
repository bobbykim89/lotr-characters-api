#!/bin/bash

echo "Install Project dependencies..."

python3 -m pip install -r requirements.txt

echo "Migrate DB..."

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static Files..."

python3 manage.py collectstatic --noinput