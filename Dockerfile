# First stage: Build environment for Tailwind CSS
FROM node:16-slim AS build
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install
COPY . /app/
RUN npm run build

# Second stage: Combined Python and Nginx environment
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for Nginx, PostgreSQL, and Python
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc libpq-dev nginx \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Copy static files generated from the build stage
COPY --from=build /app/static /app/staticfiles

# Collect static files (ensure the static folder is correctly set)
RUN python manage.py collectstatic --noinput --verbosity 2

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

RUN addgroup --system nginx && adduser --system --ingroup nginx nginx

# Ensure the entrypoint script is accessible and executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the required port for Nginx
EXPOSE 80

# Start Gunicorn and Nginx via the entrypoint script
CMD ["/app/entrypoint.sh"]
