from credentials import news_api_key
import json 
import requests
import spacy
from spacy import displacy
import en_core_web_sm
from generate_sp_500_list import sp_500_companies
nlp = en_core_web_sm.load()

endpoint = "https://newsapi.org/v2/top-headlines?language=en&country=us&"

# get the background content of the top business headlines of the day
def get_articles():
    resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
    descriptions = []
    articles = resp['articles']
    
    for i in range(0, len(articles)):
        descriptions.append(articles[i]["description"])

    return descriptions

# takes a block of text and returns a list of companies mentioned in the piece
def extract_orgs(description):
    tokens = nlp(description)
    companies = []
    for t in tokens.ents:
        # make sure the relevant company is a publicly-traded company in the sp_500
        if t.label_ == 'ORG' and t.text in sp_500_companies:
            companies.append(t.text)

    return companies

# parameters:
# content list -- The list of descriptions from the news of the day
# return: a list of related companies for the day
def news_related_tickers(article_descriptions):
    related_tickers = []
    for desc in article_descriptions:
        # at each iteration, add a list of lists of related companies
        related_tickers.append(extract_orgs(desc))

    return related_tickers