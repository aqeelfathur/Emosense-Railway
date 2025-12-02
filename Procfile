release: python manage.py migrate --noinput
web: python manage.py check && gunicorn core.wsgi --bind 0.0.0.0:$PORT --log-file - --log-level debug --timeout 120 --preload
