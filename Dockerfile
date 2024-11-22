# First stage: Build environment
FROM node:16-slim AS build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json /app/
COPY package-lock.json /app/

# Install Node.js dependencies (Tailwind, PostCSS, etc.)
RUN npm install

# Copy the rest of the app's files (for Tailwind build process)
COPY . /app/

# Run Tailwind build process
RUN npm run build

# Second stage: Python environment
FROM python:3.13-slim AS runtime

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for PostgreSQL and Python
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && apt-get clean

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code (except for build-related files)
COPY . /app/

# Copy the built static files (CSS, images, etc.) from the build stage to the Django static directory
COPY --from=build /app/static/src /app/static/src

# Copy the entrypoint.sh script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run the entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
