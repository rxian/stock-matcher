import bs4 as bs
import requests
import yfinance as yf
import time
import json

# this file is not meant to be run; it only contains the code within the jupyter notebook that was used to get the listing data
# attempting to run this code will likely result in timeouts because the yahoo finance api can't handle too many consecutive requests

sp_500_companies = []
ticker_company_name_dict = {}


def generate():
    resp = requests.get(
        'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                        headers=headers)

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace("\n", "")
        company = row.findAll('td')[1].text
        sp_500_companies.append(company)
        ticker_company_name_dict[ticker] = company


generate()
stock_data = {}
company_details = {}
counter = 0
symbol_list = list(ticker_company_name_dict.keys())
for i in range(0, len(symbol_list)):
    print(counter)
    data = yf.download(symbol_list[i], period="6mo", group_by="ticker", threads=False).to_dict('index')
    time.sleep(2)
    stock_data[symbol_list[i]] = {
        entry.isoformat()[:10]: data[entry] for entry in data.keys()}
    counter += 1

with open("sp500_130day_data.json", "w") as outfile:
    json.dump(stock_data, outfile)

for i in range(0, len(symbol_list)):
    comp = yf.Ticker(symbol_list[i])
    comp_info = comp.info
    if 'industry' not in list(comp_info.keys()):
        comp_info['industry'] = "None"
    if 'sector' not in list(comp_info.keys()):
        comp_info['sector'] = "None"
    if 'shortName' not in list(comp_info.keys()):
        comp_info['shortName'] = symbol_list[i]
    if 'longName' not in list(comp_info.keys()):
        comp_info['longName'] = symbol_list[i]
    if 'marketCap' not in list(comp_info.keys()):
        comp_info['marketCap'] = 0
    print(i)
    company_details[symbol_list[i]] = {"shortName": comp_info["shortName"], "longName": comp_info["longName"],
                                       "marketCap": comp_info["marketCap"], "industry": comp_info["industry"], "sector": comp_info["sector"]}

with open("sp500_company_info.json", "w") as outfile:
    json.dump(company_details, outfile)
