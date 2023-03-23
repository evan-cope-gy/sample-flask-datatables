FROM python:3.9-slim-bullseye

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run Flask app:
RUN python run.py

# Load sample data:
# RUN flask load_random_data

# Gunicorn Configuration
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
