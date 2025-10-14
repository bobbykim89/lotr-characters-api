#!/bin/sh
set -e

echo "Waiting for database to be ready..."
until python - <<'PY'
import os, sys
import psycopg2
import dj_database_url

try:
    db_url = os.environ.get("DB_URL")
    conn = psycopg2.connect(db_url)
    conn.close()
except Exception as e:
    sys.exit(1)
sys.exit(0)
PY
do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Database is up — make migrations"
python manage.py makemigrations

echo "running migrations"
python manage.py migrate --noinput

# --- Superuser creation ---
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
  echo "Creating Django superuser if it doesn't exist..."
  python manage.py shell <<END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
END
fi

echo "Starting Django development server on 0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000