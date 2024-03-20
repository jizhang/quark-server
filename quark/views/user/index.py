from flask import Response, jsonify, request
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from marshmallow import ValidationError

from quark import db, AppError
from quark.services import user as user_svc
from . import bp
from .schemas.login_form import login_form_schema
from .schemas.user_setting import user_setting_schema


@bp.route('/login', methods=['POST'])
def user_login() -> Response:
    form = login_form_schema.load(request.get_json())

    user = user_svc.get_by_username(form['username'])
    if user is None:
        raise AppError('Username not found')

    if not check_password_hash(user.password, form['password']):
        raise AppError('Invalid password')

    login_user(user, remember=(form['remember_me'] == '1'))

    return jsonify(id=user.id, username=user.username)


@bp.route('/setting/get')
def user_setting_get() -> Response:
    data = user_svc.get_user_setting(current_user.id)
    return jsonify(user_setting_schema.dump(data))


@bp.route('/setting/save', methods=['POST'])
def user_setting_save() -> Response:
    form = user_setting_schema.load(request.get_json())
    user_svc.save_user_setting(current_user.id, form)
    db.session.commit()
    return jsonify({})
