import os
from main.report_chart import report_chart
from main import create_app

config_name = os.getenv('FLASK_CONFIG') or 'development'
app = create_app(config_name)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)
    #threaded=True