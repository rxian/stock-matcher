import requests
from news import News
from credentials import endpoint, news_api_key

# def get_description(url):
#     resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
#     articles = resp['articles']
    
#     for i in range(0, len(articles)):
#         if articles[i]["url"] == url:
#             return articles[i]["description"]
    
#     return "Not found"

# def get_title(url):
#     resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
#     articles = resp['articles']
    
#     for i in range(0, len(articles)):
#         if articles[i]["url"] == url:
#             return articles[i]["title"]
    
#     return "Not found"

def get_info():
    resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
    articles = resp['articles']
    news_info_list = []
    for i in range(0, len(articles)):
        news_article = News(articles[i]["url"], articles[i]["description"], articles[i]["title"], articles[i]["publishedAt"])
        news_info_list.append(news_article)
    return news_info_list

