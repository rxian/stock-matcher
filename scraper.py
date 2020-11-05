import bs4 as bs
import pickle
import json
import requests
from credentials import api_key
import datetime as dt
import csv
import time

historical_price_endpoint = "https://cloud.iexapis.com/stable/stock/"
# get all current s&p 500 tickers
def get_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                        headers=headers)
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker.replace("\n", ""))
    return tickers

# a general that allows us to pull historical data
def get_historical_data(ticker, duration):
    response = requests.get(historical_price_endpoint + ticker.lower() + "/chart/" + duration + "?token=" + api_key)
    json_response = response.json()
    return json_response

# generate our dataset
def generate_csv():
    with open('stockData.csv', 'w', newline='') as file:
        fieldnames = ['symbol', 'date', 'open', 'close', 'high', 'low', 'volume']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for ticker in get_sp500_tickers():
            time.sleep(1)
            for i in range(0, len(get_historical_data(ticker, "3m"))):
                writer.writerow({
                    'symbol': ticker.lower(), 
                    'date': get_historical_data(ticker, "3m")[i]['date'],
                    'open': get_historical_data(ticker, "3m")[i]['open'],
                    'close': get_historical_data(ticker, "3m")[i]['close'],
                    'high': get_historical_data(ticker, "3m")[i]['high'],
                    'low': get_historical_data(ticker, "3m")[i]['low'],
                    'volume': get_historical_data(ticker, "3m")[i]['volume']
                })

generate_csv()