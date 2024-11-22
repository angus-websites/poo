#!/bin/bash

# Run Django database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start Gunicorn in the background
echo "Starting Gunicorn..."
gunicorn poo.wsgi:application --bind unix:/app/gunicorn.sock --workers 3 --timeout 300 &

# Start Nginx
echo "Starting Nginx..."
nginx -g "daemon off;"
