#!/bin/bash
set -e

if [[ -z "$@" ]]; then
   echo "[Postgres] warming up..."
   sleep 10

   echo "[Django] collecting statics..."
   pipenv run python manage.py collectstatic --noinput --clear

   echo "[Django] migrating..."
   pipenv run python manage.py migrate

   echo "[Gunicorn] running..."
   pipenv run gunicorn --bind 0.0.0.0:$FAST_WEBAPP_PORT --log-level=error fast_web_backend.wsgi:application
else
  exec $@
fi
