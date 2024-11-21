#!/bin/bash

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files (if necessary)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn poo.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 300
