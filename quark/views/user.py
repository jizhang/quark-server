from flask import Blueprint, Response, jsonify, request
from flask_login import login_user
from werkzeug.security import check_password_hash

from quark import AppError
from quark.services import user as user_svc

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/login', methods=['POST'])
def user_login() -> Response:
    user = user_svc.get_by_username(request.json['username'])
    if user is None:
        raise AppError('Username not found')

    if not check_password_hash(user.password, request.json['password']):
        raise AppError('Invalid password')

    login_user(user, remember=(request.json['remember_me'] == '1'))

    return jsonify(id=user.id, username=user.username)
