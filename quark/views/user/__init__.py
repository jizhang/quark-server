from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/api/user')

from . import index
