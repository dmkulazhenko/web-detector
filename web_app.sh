#!/bin/sh

python ./mysql_waiter.py

flask db init -d "$SQLALCHEMY_MIGRATIONS_DIR"
if [ "x$1" = "xtrue" ]; then
  flask db migrate -d "$SQLALCHEMY_MIGRATIONS_DIR"
fi
flask db upgrade -d "$SQLALCHEMY_MIGRATIONS_DIR"

exec gunicorn -b :5000 --reload --workers 5 --threads 2 --timeout 60 --access-logfile - --error-logfile - web_app:app
