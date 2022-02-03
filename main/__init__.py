# app/__init__.py

# third-party imports
from flask import Flask

# local imports
from config import app_config
from flask_login import LoginManager

login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    #temporary route
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    #temporary route
    @app.route('/dcf')
    def hello_world2():
        return 'Hello, World!2'
    return app