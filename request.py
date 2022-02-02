import requests
from utils import getLogger

DEBUG = getLogger()

HEADER = {'user-agent': 'PostmanRuntime/7.26.10', 'Connection': 'keep-alive'}

def get_nasdaq_institution_from_api(stock):
  # my_headers = {'user-agent': 'PostmanRuntime/7.26.10', 'Connection': 'keep-alive'}
  url = "https://api.nasdaq.com/api/company/" + stock + "/institutional-holdings?limit=0&sortColumn=marketValue&sortOrder=DESC"
  result = call_api(url)
  return result

def get_employment_data():
  url = "https://www.macromicro.me/charts/data/6,65,171,172,173,20,3578,6707,20499,20500,389,20509,20511,20512,87,36,19,18,20313,1952,23622,33391"
  result = call_api(url)
  return result

def call_api(url):
  try:
    response =requests.get(url, headers = HEADER)
    return response.json()
  except Exception as error:
    DEBUG.error("{}".format(error))
    return None
