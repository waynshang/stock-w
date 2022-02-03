from utils import getLogger
DEBUG = getLogger()
import os

from main import create_app

config_name = os.getenv('FLASK_CONFIG')
DEBUG.info(config_name)
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)