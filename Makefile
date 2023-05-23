default: web

web:
	poetry run flask --app quark run --debug

prod:
	poetry install --extras gunicorn --without dev
