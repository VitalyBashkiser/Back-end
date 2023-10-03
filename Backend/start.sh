#!/bin/sh

# Apply migrations
python manage.py migrate

# Start the server
python manage.py runserver 0.0.0.0:8000

