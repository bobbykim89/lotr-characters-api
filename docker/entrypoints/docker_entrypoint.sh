#!/bin/sh
set -e

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