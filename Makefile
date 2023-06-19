default: web

dev:
	poetry install

web:
	poetry run flask --app quark run --debug

test:
	poetry run ruff quark tests
	poetry run mypy quark tests
	poetry run pytest tests

prod:
	poetry install --extras gunicorn --without dev
