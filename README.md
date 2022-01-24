# ds-judgements-public-access-service

1. Copy `ds_judgements_public_access_service/.env.example` to `ds_judgements_public_access_service/.env`
2. `cd ds_judgements_public_access_service/`
3. `pip install -r requirements/local.txt`
4. `createdb ds_judgements_public_access_service -U postgres --password admin`
5. `export DATABASE_URL=postgres://postgres:admin@127.0.0.1:5432/ds_judgements_public_access_service`
6. `export DJANGO_READ_DOT_ENV_FILE=True`
7. `python manage.py migrate`
8. `python manage.py runserver 0.0.0.0:8000`