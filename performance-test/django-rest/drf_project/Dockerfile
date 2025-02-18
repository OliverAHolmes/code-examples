FROM python:3.12-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY drf_project /app/drf_project

# Expose the port
EXPOSE 8000

# Use gunicorn for production-like environment
CMD ["gunicorn", "drf_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
