#!/bin/sh

# Wait for the database to become available
/wait-for-it.sh db:5432 -- python manage.py migrate

# Start the server
python manage.py runserver 0.0.0.0:8000

