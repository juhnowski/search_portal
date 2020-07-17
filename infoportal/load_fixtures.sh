#!/bin/sh

export DJANGO_SETTINGS_MODULE=settings.common

python --version

echo "run makemigrations"
python manage.py makemigrations users documents search notes folders analytics integration search

echo "run migrate"
python manage.py migrate

echo "load fixtures"
python manage.py loaddata fixtures/users.json --app users
python manage.py loaddata fixtures/documents.json --app documents
python manage.py loaddata fixtures/notes.json --app notes
python manage.py loaddata fixtures/folders.json --app folders
python manage.py loaddata fixtures/analytics.json --app analytics
python manage.py loaddata fixtures/import_journal.json --app integration

