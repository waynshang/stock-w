from flask import Blueprint

dcf = Blueprint('dcf', __name__)

from . import views

