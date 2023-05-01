from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import default_settings

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(default_settings)
    app.config.from_envvar('APP_CONFIG', silent=True)

    db.init_app(app)

    from .views import account
    app.register_blueprint(account.bp)

    return app
