#!/bin/sh

# Apply migrations
python Backend/manage.py migrate

# Start the server
python Backend/manage.py runserver 127.0.0.1:8000
