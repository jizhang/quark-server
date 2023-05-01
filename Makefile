default: web

web:
	poetry run flask --app quark run --debug
