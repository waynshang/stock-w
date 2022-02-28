# app/__init__.py

# third-party imports
from flask import Flask

# local imports
from main.config import app_config
from .report_chart import report_chart


def create_app(config_name):
    app = Flask(__name__)
    # app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')

    #temporary route
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    #register
    app.register_blueprint(report_chart, url_prefix='/report_chart', template_folder='templates')
    return app