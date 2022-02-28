from flask import Blueprint

from .controllers import index, show
report_chart = Blueprint('report_chart', __name__)

report_chart.route('/', methods=['GET'])(index)
report_chart.route('/<ticker>', methods=['GET'])(show)

