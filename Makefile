default: web

dev:
	poetry install

web:
	poetry run flask --app quark run --debug

test:
	poetry run ruff quark

prod:
	poetry install --extras gunicorn --without dev
