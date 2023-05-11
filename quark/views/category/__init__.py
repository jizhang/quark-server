from flask import Blueprint

bp = Blueprint('category', __name__, url_prefix='/api/category')

from . import index
