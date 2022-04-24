# stock-w
if have come up with any idea about stock will be add to this project

API
1. return revenue, gross profit, free cash and flow operating expense chart of stock
  method: get
  url: host/report_chart/{stock_symbol}
  parameter
  - frequency (ANNUAL, QUARTERLY)
2. return beta, annual revenue, stdev, sharpe ratio of stocks, duration default 1 year
  method: get
  url: host/risk
  parameter
  - tickers ex aapl,tsla
  - start date
  - end date
  - duration
  - frequency
