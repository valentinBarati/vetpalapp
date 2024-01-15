FROM python:3.9.18-bookworm

# Install system dependencies
RUN apt-get update \
    && apt-get install -y wkhtmltopdf \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app/main

# Install Python dependencies
RUN pip install psycopg2-binary
RUN pip install Django==3.2.23
RUN pip install django-wkhtmltopdf
RUN pip install django-seed
RUN pip install django-bootstrap-v5
RUN pip install fontawesomefree
