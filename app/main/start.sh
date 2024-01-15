#!/bin/sh

FLAG_FILE="/usr/src/app/.initialized"

if [ ! -f "$FLAG_FILE" ]; then
    python /usr/src/app/main/manage.py makemigrations
    python /usr/src/app/main/manage.py migrate
    python /usr/src/app/main/manage.py seed_data
    touch "$FLAG_FILE"
fi

# Start the application 
python manage.py runserver 0.0.0.0:8000