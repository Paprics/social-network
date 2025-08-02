#!/bin/bash

python manage.py migrate
python manage.py check
python manage.py collectstatic --no-input

#python src/manage.py runserver 0.0.0.0:8000
gunicorn -w${WSGI_WORKERS} -b 0.0.0.0:${WSGI_PORT} --chdir /app/src config.wsgi:application --log-level ${WSGI_LOG_LEVEL}

