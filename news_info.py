import requests
from credentials import endpoint, news_api_key

def get_description(url):
    resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
    articles = resp['articles']
    
    for i in range(0, len(articles)):
        if articles[i]["url"] == url:
            return articles[i]["description"]
    
    return "Not found"

def get_title(url):
    resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
    articles = resp['articles']
    
    for i in range(0, len(articles)):
        if articles[i]["url"] == url:
            return articles[i]["title"]
    
    return "Not found"