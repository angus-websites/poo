#!/bin/bash

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2

# Start Gunicorn in the background
echo "Starting Gunicorn..."
gunicorn poo.wsgi:application --bind unix:/app/gunicorn.sock --workers 3 --timeout 300 &

# Start Nginx
echo "Starting Nginx..."
nginx -g "daemon off;"
