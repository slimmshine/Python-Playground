from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# In the parameters place all the tickers that you want to get
parameters = {
  'symbol':'BTC,ETH,ADA,DOGE,DOT,UNI,SOL,LINK,MATIC,THETA,VET,AVAX,AXS,'\
           'AAVE,ALGO,ATOM',
  'aux': 'max_supply,circulating_supply,total_supply,cmc_rank'

}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'YOUR-API-KEY',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
  with open('prices.json', 'w') as outfile:
      json.dump(data, outfile)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
