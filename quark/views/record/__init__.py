from flask import Blueprint

bp = Blueprint('record', __name__, url_prefix='/api/record')

from . import edit, index
