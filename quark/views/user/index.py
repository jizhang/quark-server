from flask import Response, jsonify, request
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from marshmallow import ValidationError

from quark import db, AppError
from quark.services import user as user_svc
from . import bp
from .schemas.user_setting import user_setting_schema


@bp.route('/login', methods=['POST'])
def user_login() -> Response:
    user = user_svc.get_by_username(request.json['username'])
    if user is None:
        raise AppError('Username not found')

    if not check_password_hash(user.password, request.json['password']):
        raise AppError('Invalid password')

    login_user(user, remember=(request.json['remember_me'] == '1'))

    return jsonify(id=user.id, username=user.username)


@bp.route('/setting/get')
def user_setting_get() -> Response:
    data = user_svc.get_user_setting(current_user.id)
    return jsonify(user_setting_schema.dump(data))


@bp.route('/setting/save', methods=['POST'])
def user_setting_save() -> Response:
    try:
        form = user_setting_schema.load(request.json)
    except ValidationError as e:
        raise AppError(str(e.messages))

    user_svc.save_user_setting(current_user.id, form)
    db.session.commit()
    return jsonify({})
