# First stage: Build environment for Tailwind CSS
FROM node:16-slim AS build
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install
COPY . /app/
RUN npm run build

# Second stage: Python environment for Django and Gunicorn
FROM python:3.13-slim AS python-base
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Collect static files
COPY --from=build /app/static /app/staticfiles
RUN python manage.py collectstatic --noinput --verbosity 2

# Third stage: Production environment with Nginx
FROM nginx:alpine AS production
WORKDIR /app

# Copy application code and static files from python-base stage
COPY --from=python-base /app /app

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Ensure the entrypoint script is accessible
COPY entrypoint.sh /app

# Expose the required port for Nginx
EXPOSE 80

# Set the entrypoint script as executable
RUN chmod +x /app/entrypoint.sh

# Start Nginx and Gunicorn
CMD /bin/sh /app/entrypoint.sh
