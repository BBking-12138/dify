from flask import Blueprint

from libs.external_api import ExternalApi

bp = Blueprint('stock_api', __name__, url_prefix='/stock')
api = ExternalApi(bp)


from . import index
from .app import app