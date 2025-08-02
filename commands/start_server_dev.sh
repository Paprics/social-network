#!/bin/bash

python manage.py migrate
python manage.py check
#python src/manage.py runserver 0.0.0.0:8000
uvicorn config.asgi:application --host 0.0.0.0 --port 8000


##!/bin/bash
#
#echo "DEBUG: Current directory: $(pwd)"
#echo "DEBUG: Listing files:"
#ls -la
#
#echo "DEBUG: Working directory set in Docker: $PWD"
#
#echo "DEBUG: Environment variables:"
#env | sort
#
#python manage.py migrate
#python manage.py check
#
#echo "DEBUG: Starting uvicorn with:"
#echo "uvicorn config/asgi:application --host 0.0.0.0 --port 8000"
#
#uvicorn config.asgi:application --host 0.0.0.0 --port 8000
#
