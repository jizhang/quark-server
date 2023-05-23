from flask import Blueprint

bp = Blueprint('chart', __name__, url_prefix='/api/chart')

from . import index
