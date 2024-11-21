# pull official base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for PostgreSQL and other packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && apt-get clean

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Copy the entrypoint.sh script into the container and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run the entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
