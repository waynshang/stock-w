from flask import render_template, abort, request
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

from utils import get_keys, get_values, create_dict_from_variables

ANNUAL = 'annual'
QUARTERLY = 'quarterly'
FREQUENCY_OPTIONS = [ANNUAL, QUARTERLY]
INCOME = 'income'
CASH = 'cash'
BALANCE= 'balance'
YEARLY_STATEMENTS_OPTIONS_KEYS = ['incomeStatementHistory','cashflowStatementHistory', 'balanceSheetHistory']
QUARTERLY_STATEMENTS_OPTIONS_KEYS = ['incomeStatementHistoryQuarterly', 'cashflowStatementHistoryQuarterly', 'balanceSheetHistoryQuarterly']

OPERATING_EXPENSES= 'totalOperatingExpenses'
REVENUE = 'totalRevenue'
GROSS_PROFIT = 'grossProfit'
TOTAL_CASH = 'totalCashFromOperatingActivities'
CAPITAL_EXPENDITURES = 'capitalExpenditures'

GROSS_PROFIT_RATE = 'gross_profit_rate'
FREE_CASH_FLOW = 'free_cash_flow'

def index():
    return "please input a ticker"

def show(ticker):
  DEBUG.info(ticker)
  global STATEMENTS_OPTIONS
  global frequency
  frequency = request.args.get('frequency')
  frequency = frequency if frequency in FREQUENCY_OPTIONS else ANNUAL
  if frequency == ANNUAL: 
    STATEMENTS_OPTIONS = create_dict_from_variables([INCOME,CASH,BALANCE], YEARLY_STATEMENTS_OPTIONS_KEYS)
  else:
    STATEMENTS_OPTIONS = create_dict_from_variables([INCOME,CASH,BALANCE], QUARTERLY_STATEMENTS_OPTIONS_KEYS)

  DEBUG.info(frequency)
  ticker = ticker.upper()
  yf_ticker = yf.Ticker(ticker)
  try:  
    info = yf_ticker.info
  except:
    DEBUG.error(f"invalid ticker: {ticker}")  
    abort(404)
  try:
    yahoo_financials = YahooFinancials(ticker)
    print(get_keys(STATEMENTS_OPTIONS))
    all_statement_data_qt =  yahoo_financials.get_financial_stmts(frequency, get_keys(STATEMENTS_OPTIONS))
    all_data = get_all_data(ticker, all_statement_data_qt)
    DEBUG.info(all_data)
    # price_history = get_stock_price_history(ticker, commence_date, end_date, length = 'year')
    image_urls = draw_images(all_data)
  
    return render_template('report_chart/template.html', 
      revenue_url=image_urls[REVENUE], 
      gross_profit_rate_url = image_urls[GROSS_PROFIT_RATE], 
      free_cash_flow_url = image_urls[FREE_CASH_FLOW],
      operating_expenses_url = image_urls[OPERATING_EXPENSES])

  except TemplateNotFound as e:
    DEBUG.error(e)  
    abort(404)
   
#private
def get_stock_price_history(ticker, commence_date, end_date, length = 'year'):
    aapl_df = ticker.history(period="5y")

def get_all_data(ticker, all_statement_data_qt):
  print(all_statement_data_qt)
  income_history_date = all_statement_data_qt[STATEMENTS_OPTIONS[INCOME]][ticker]
  cash_history_date = all_statement_data_qt[STATEMENTS_OPTIONS[CASH]][ticker]
  balance_history_date = all_statement_data_qt[STATEMENTS_OPTIONS[BALANCE]][ticker]

  #revenue
  labels = REVENUE
  revenue_data = get_history_data(income_history_date, labels)
  #gross_profit_rate
  labels = create_dict_from_variables([GROSS_PROFIT], [REVENUE])
  gross_profit_rate_data = get_history_data(income_history_date, labels)
  #free cash flow
  labels = [TOTAL_CASH, CAPITAL_EXPENDITURES]
  free_cash_flow_data = get_history_data(cash_history_date, labels)
  #operating expenses
  labels = OPERATING_EXPENSES
  operating_expenses_data = get_history_data(income_history_date, labels)
  return create_dict_from_variables(
    [REVENUE, GROSS_PROFIT_RATE, FREE_CASH_FLOW, OPERATING_EXPENSES], 
    [revenue_data, gross_profit_rate_data, free_cash_flow_data, operating_expenses_data]
  )


def get_history_data(history_date, labels):
  return list(reversed(list(map(get_date_value_dict, history_date, repeat(labels)))))


# def draw_cash_plot(ticker, labels):
#   date_value_dict = map(get_date_value_dict, financial_cash['cashflowStatementHistory'][ticker], repeat(labels))
#   date_value_dict = list(reversed(list(date_value_dict)))
#   print(date_value_dict)

#   plt.plot(get_keys(date_value_dict), get_values(date_value_dict))
#   plt.xticks(get_keys(date_value_dict))
#   plt.show()

def get_date_value_dict(ticker_data, label):
  key = get_keys(ticker_data)[0]
  value = ticker_data[key]
  if type(label) == list:
    data = value[label[0]]
    for index, l in enumerate(label):
      if index == 0: pass
      data -= value[l]
  elif type(label) ==dict:
    label_key = get_keys(label)[0] or 0
    label_value = label[label_key] or 0
    data = value[label_key] / value[label_value] * 100
  else: 
    data = value[label]
  if frequency == ANNUAL:
    key = key[0:4]
  else:
    key = key[0:7]
  return {key: data}

def draw_images(data):
  image_urls = []
  for key in data:
    img = BytesIO()
    d = data[key]

    plot_url = ''
    plt.figure()
    plt.plot(get_keys(d), get_values(d))
    plt.xticks(get_keys(d))
    plt.title(f'{key}')
    plt.savefig(img, format='png')
    plot_url = base64.b64encode(img.getvalue())
    # img.seek(0)
    image_urls.append(plot_url.decode('utf8'))

  return create_dict_from_variables(
    [REVENUE, GROSS_PROFIT_RATE, FREE_CASH_FLOW, OPERATING_EXPENSES], 
    image_urls
  )