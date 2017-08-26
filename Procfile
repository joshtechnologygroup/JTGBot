web: newrelic-admin run-program uwsgi --ini wsgi.ini --http-socket :$PORT
scheduler: celery -A bot worker  -B -l info
