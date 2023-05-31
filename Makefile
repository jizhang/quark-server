default: web

dev:
	poetry install

web:
	poetry run flask --app quark run --debug

test:
	poetry run ruff quark
	poetry run mypy quark

prod:
	poetry install --extras gunicorn --without dev
