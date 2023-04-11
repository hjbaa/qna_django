#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Очистка БД
#python manage.py flush --no-input
# Запуск миграций
#python manage.py migrate

exec "$@"
