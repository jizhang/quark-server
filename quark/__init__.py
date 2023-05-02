from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

from . import default_settings

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(default_settings)
    app.config.from_envvar('APP_CONFIG', silent=True)

    db.init_app(app)


    @app.errorhandler(AppError)
    def handle_app_error(e: AppError) -> Response:
        payload = {
            'code': e.code,
            'message': e.message,
        }
        return jsonify(payload), 400


    from .views import account
    app.register_blueprint(account.bp)

    return app


class AppError(Exception):
    def __init__(self, message: str, code=400):
        super().__init__(message)
        self.message = message
        self.code = code
