from flask import Blueprint

from .controllers import index
risk = Blueprint('risk', __name__)

risk.route('/', methods=['GET'])(index)
# report_chart.route('/<ticker>', methods=['GET'])(show)

