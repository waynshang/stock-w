from flask import render_template, abort
# from flask_login import login_required
from utils import getLogger
DEBUG = getLogger()
from . import dcf

import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials

from io import StringIO, BytesIO
import base64

from jinja2 import TemplateNotFound

@dcf.route('/')
def homepage():
    return "DCF"

@dcf.route('/<stock_symbol>')
def get_dcf(stock_symbol):
    print(stock_symbol)
    ticker = yf.Ticker('AAPL')
    aapl_df = ticker.history(period="5y")
    img = BytesIO()
    plt = aapl_df['Close'].plot(title="APPLE's stock price")
    plt.figure.savefig(img, format='png')
    # img.seek(0)

    plot_url = base64.b64encode(img.getvalue())
    try:
        return render_template('dcf/template.html', plot_url=plot_url.decode('utf8')) 
    except TemplateNotFound as e:
        DEBUG.error(e)  
        abort(404)
    # return "123"

   
