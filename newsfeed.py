from credentials import news_api_key
import json 
import requests

endpoint = "https://newsapi.org/v2/top-headlines?language=en&country=us&"

# get the background content of the top business headlines of the day
def get_articles():
    resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
    descriptions = []
    articles = resp['articles']
    
    for i in range(0, len(articles)):
        descriptions.append(articles[i]["description"])

    return descriptions


