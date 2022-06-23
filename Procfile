web: gunicorn core.wsgi:application --log-file - --log-level debug --preload
python manage.py collectstatic --noinput
manage.py migrate
