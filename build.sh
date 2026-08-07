#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files for WhiteNoise..."
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate
