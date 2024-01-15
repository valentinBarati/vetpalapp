# VetPalApp

## Overview

VetPalApp is a Django-based web application designed to streamline veterinary clinic management. This project is built using Python 3.9.1, Django 3.2.23, and relies on PostgreSQL as its database.

## Prerequisites

Ensure you have the following installed:

- Python 3.9.1
- Django 3.2.23
- PostgreSQL

A `.env` file is present in the project root with the following configuration:

```plaintext
POSTGRES_DB=vetpalapp
POSTGRES_USER=vetpalapp
POSTGRES_PASSWORD=j0stP4sw0rd113
```

## Getting Started

### Running with Docker Compose

To run the application using Docker Compose, execute the following command in the project root:

```bash
docker-compose up
```
#### Default Superuser

The default superuser credentials are:

- Username: test
- Password: test

### Manual Steps

In case of issues or for specific tasks, follow these manual steps:

#### 1. Database Migrations:

```bash
docker exec -ti vet_app python /usr/src/app/main/manage.py makemigrations
docker exec -ti vet_app python /usr/src/app/main/manage.py migrate
```

#### 2. Seed Data:

```bash
docker exec -ti vet_app python /usr/src/app/main/manage.py seed_data
```

#### 3. Create Superuser:

```bash
docker exec -ti vet_app python /usr/src/app/main/manage.py createsuperuser
```


### Troubleshooting
If any issues arise, restarting the application using the following command may resolve them:

```bash
docker-compose restart
```

### Additional Information

- The main application folder contains a start.sh script, which is the entry point for the application.
- If the database is not up, and start.sh has already created an .initialized file (indicating migrations and seeders have run), you can `manually` perform the required steps mentioned above.