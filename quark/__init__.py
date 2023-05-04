from typing import Optional

from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from . import default_settings

db = SQLAlchemy()
login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(default_settings)
    app.config.from_envvar('APP_CONFIG', silent=True)

    db.init_app(app)
    configure_login_manager(app)
    configure_views(app)

    @app.errorhandler(AppError)
    def handle_app_error(e: AppError) -> Response:
        payload = {
            'code': e.code,
            'message': e.message,
        }
        return jsonify(payload), 400

    return app


def configure_login_manager(app: Flask):
    login_manager.init_app(app)

    from quark.models.user import User
    from quark.services import user as user_svc

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        return user_svc.get_user(user_id)


def configure_views(app: Flask):
    from .views import account, user
    app.register_blueprint(account.bp)
    app.register_blueprint(user.bp)


class AppError(Exception):
    def __init__(self, message: str, code=400):
        super().__init__(message)
        self.message = message
        self.code = code
