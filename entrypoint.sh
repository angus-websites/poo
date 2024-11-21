#!/bin/bash

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn poo.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 300
