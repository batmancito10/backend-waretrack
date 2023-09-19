#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py creategroups
python manage.py createcompany
python manage.py createsupply
python manage.py createproduts