from flask import render_template, abort, request, jsonify
from flask_login import login_required
from debugger import getLogger
import matplotlib as mpl
import matplotlib.pyplot as plt
DEBUG = getLogger()
from itertools import repeat

import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials

from io import BytesIO
import base64
from jinja2 import TemplateNotFound

from datetime import datetime, timedelta
import nasdaqdatalink
from statistics import stdev , mean
from math import sqrt

from utils import get_keys, get_values, create_dict_from_variables

ANNUAL = 'annual'
QUARTERLY = 'quarterly'
DURATION_DAYS = {
  ANNUAL:365,
  QUARTERLY: 90
}
DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'
FREQUENCY_OPTIONS = [DAILY, WEEKLY, MONTHLY]
TEN_YEAR_BOND_YIELD = "FRED/DGS10"
TRADING_DAY_A_YEAR =252
DATE_FORMAT= "%Y-%M-%d"

def index():
  global frequency
  tickers =(request.args.get('tickers') or '').split(',')
  frequency = request.args.get('frequency')
  start_date = request.args.get('start_date') or (datetime.now() - timedelta(days=365)).strftime(DATE_FORMAT)
  end_date = request.args.get('end_date') or (datetime.now()).strftime(DATE_FORMAT)
  duration = request.args.get('duration') or ANNUAL
  split_dates = _split_date(start_date, end_date, duration)
  frequency = frequency if frequency in FREQUENCY_OPTIONS else DAILY

  risk_datas = []
  DEBUG.info(f"frequency: {frequency}")
  for split_date in split_dates:
    start_date = split_date['start_date']
    end_date = split_date['end_date']

    DEBUG.info(f"start_date: {start_date}")
    DEBUG.info(f"end_date: {end_date}")

    risk_data = {'start_date': start_date, 'end_date': end_date}
    risk_rate = mean(list(map(lambda x: x[1],(nasdaqdatalink.get("FRED/DGS10" , start_date=start_date, end_date=end_date, returns="numpy")))))

    for ticker in tickers:
      ticker = ticker.upper()
      yf_ticker = yf.Ticker(ticker)
      try:  
        info = yf_ticker.info
      except:
        DEBUG.error(f"invalid ticker: {ticker}")
        tickers.remove(ticker)
        # abort(404)
    
      try:
        yahoo_financials = YahooFinancials(ticker)
        price_date = yahoo_financials.get_historical_price_data(start_date, end_date, frequency)
        price_changes = _get_stock_price_change_history(ticker, price_date)
        DEBUG.info(price_changes)
        annual_revenue = mean(price_changes) * TRADING_DAY_A_YEAR * 100 if price_changes else 0
        stdev_per_annual = stdev(price_changes) * sqrt(TRADING_DAY_A_YEAR) * 100 if price_changes else 0

        sharpe_ratio = (annual_revenue - risk_rate ) / stdev_per_annual if stdev_per_annual and stdev_per_annual != 0 else 0
        risk_data[ticker] = {
          'beta': yahoo_financials.get_beta(), 
          'annual_revenue': annual_revenue,  
          'stdev_per_annual': stdev_per_annual, 
          'sharpe_ratio': sharpe_ratio }

        # image_urls = draw_images(price_changes)
      
      except TemplateNotFound as e:
        DEBUG.error(e)  
        abort(404)
    risk_datas.append(risk_data)

  DEBUG.info(risk_datas)
  return jsonify({'result': risk_datas})
  # render_template('risk/template.html', 
      # data=price_changes)

   
#private

def _get_stock_price_change_history(ticker, price_date, price_type = 'close'):
  if 'prices' not in price_date[ticker]:
    return None
  prices_data = price_date[ticker]['prices']
  price_changes = []
  
  for index, price in enumerate(prices_data):
    # date = price['formatted_date']
    prev_price = prices_data[index-1][price_type] if index > 0 else price[price_type]
    change = (price[price_type] - prev_price) / prev_price
    
    if index > 0: price_changes.append(change)
  return price_changes

def _split_date(start_date, end_date, duration = ANNUAL):
  split_days= []
  start_date = datetime.strptime(start_date, DATE_FORMAT)
  end_date = datetime.strptime(end_date, DATE_FORMAT)

  diff_days = (end_date - start_date).days
  if diff_days > DURATION_DAYS[duration]:
    real_start_date = start_date.strftime(DATE_FORMAT)
    real_end_date = ( start_date + timedelta(days=DURATION_DAYS[duration])).strftime(DATE_FORMAT)
    split_days.append({'start_date': real_start_date, 'end_date': real_end_date})

    next_start_date = ( start_date + timedelta(days=DURATION_DAYS[duration]+1)).strftime(DATE_FORMAT)
    next_end_date = end_date.strftime(DATE_FORMAT)

    split_days += _split_date(next_start_date, next_end_date, duration)
  
  real_start_date = start_date.strftime(DATE_FORMAT)
  real_end_date = end_date.strftime(DATE_FORMAT)
  split_days.append({'start_date': real_start_date, 'end_date': real_end_date})
  return split_days




