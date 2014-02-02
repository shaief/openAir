web: python manage.py run_gunicorn -b 0.0.0.0:$PORT
worker: celery -A tasks worker -B --loglevel=info