from bs4 import BeautifulSoup
import requests
import json
import datetime
from news import News
import csv
from write_data import *
from database import driver, GraphDatabase

# this file is not meant to be run; it only contains the code within the jupyter notebook that was used to get the article data

with open('sp500_company_info.json') as f:
    data = json.load(f)

company_symbols = list(data.keys())

# this was originally used to pull articles from nasdaq and yahoo, which proved to be too slow
# headers = {
#     'User-Agent': "PostmanRuntime/7.26.5",
#     'Connection': "keep-alive"
# }
# article_list = []
# for key in company_symbols:
#     url = 'https://www.nasdaq.com/feed/rssoutbound?symbol={symbol}'.format(symbol = key)
#     resp = requests.get(url, headers=headers)
#     soup = BeautifulSoup(resp.content, 'xml')
#     for article in soup.find_all("item"):
#         mentioned_companies = []
#         if article.tickers:
#             mentioned_companies = article.tickers.text.split(',')
#         else:
#             mentioned_companies = [key]
#         news_article = News(article.link.text, mentioned_companies, article.title.text, article.pubDate.text)
#         article_list.append(news_article)
#     url = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US'.format(symbol = key)
#     resp = requests.get(url, headers=headers)
#     soup = BeautifulSoup(resp.content, 'xml')
#     for article in soup.find_all("item"):
#         mentioned_companies = [key]
#         news_article = News(article.link.text, mentioned_companies, article.title.text, article.pubDate.text)
#         article_list.append(news_article)
#     print(key)

# get articles from the nasdaq article rss feed
headers = {
    'User-Agent': "PostmanRuntime/7.26.5",
    'Connection': "keep-alive"
}
nasdaq_article_list = []
count = 0
for key in company_symbols:
    url = 'https://www.nasdaq.com/feed/rssoutbound?symbol={symbol}'.format(symbol = key)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'xml')
    for article in soup.find_all("item"):
        mentioned_companies = []
        if article.tickers:
            mentioned_companies = article.tickers.text.split(',')
        mentioned_companies.append(key)
        timestamp = article.pubDate.text
        timestamp = timestamp[timestamp.find(", ") + 2:timestamp.find("+") - 1]
        date_time_obj = datetime.datetime.strptime(timestamp, '%d %b %Y %H:%M:%S')
        news_article = News(article.link.text, mentioned_companies, article.title.text, date_time_obj.strftime('%Y-%m-%dT%H:%M:%S'))
        nasdaq_article_list.append(news_article)
    count += 1
    print(count)

company_info = {}
with open('Listings.csv', newline='') as csvfile:
    companies = csv.reader(csvfile)
    companies.__next__()
    for row in companies:
        print(row[1])
        company_info[row[0]] = {"symbol": row[1], "name": row[2], "industry": data[row[1]]["industry"], "sector": data[row[1]]["sector"], "market_cap": data[row[1]]["marketCap"]}

# insert data into the neo4j database
# write_data.insert_listings(company_info)
# write_data.insert_news(nasdaq_article_list)