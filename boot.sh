export CRUD_SERVER_ENV=prod
CWD=$(pwd)
export PYTHONPATH="${PYTHONPATH}:$CWD"

gunicorn server:app --access-logfile "-" --timeout 3600