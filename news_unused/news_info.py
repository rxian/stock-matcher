# this file is unused, but can be useful for future improvements to the news article data collection

# import requests
# import json
# import spacy
# from spacy import displacy
# import en_core_web_sm
# from news import News
# from credentials import endpoint, news_api_key

# nlp = en_core_web_sm.load()

# # takes a block of text and returns a list of companies mentioned in the piece
# def extract_orgs(description: str, nasdaq_symbols_companies: dict) -> list:
#     tokens = nlp(description)
#     companies = []
#     for t in tokens.ents:
#         # make sure the relevant company is a publicly-traded company in the sp_500
#         if t.label_ == 'ORG':
#             company_name = [name for name in nasdaq_symbols_companies.values() if t.text in name]
#             if company_name:
#                 companies.append(company_name[0])
#     return companies

# # parameters:
# # content list -- The list of descriptions from the news of the day
# # nasdaq_symbols_companies -- A dict with a symbol as a key and company name as a value
# # return: a list of related companies for the day
# def get_related_companies(article_descriptions: list, nasdaq_symbols_companies: dict) -> list:
#     related_companies = []
#     for desc in article_descriptions:
#         # at each iteration, add a list of lists of related companies
#         related_companies.append(extract_orgs(desc, nasdaq_symbols_companies))
#     return related_companies


# def get_info(nasdaq_symbols_companies: dict) -> list:
#     resp = requests.get(endpoint + "category=business&apiKey=" + news_api_key).json()
#     articles = resp['articles']
#     news_info_list = []
#     for i in range(0, len(articles)):
#         relevant_info = ""
#         if articles[i]["title"] and articles[i]["description"]:
#             relevant_info = articles[i]["title"] + " " + articles[i]["description"]
#         elif articles[i]["title"] and not articles[i]["description"]:
#             relevant_info = articles[i]["title"]
#         elif not articles[i]["title"] and articles[i]["description"]:
#             relevant_info = articles[i]["description"]
#         if relevant_info != "":
#             news_article = News(articles[i]["url"], articles[i]["description"], extract_orgs(relevant_info, nasdaq_symbols_companies), articles[i]["title"], articles[i]["publishedAt"])
#             news_info_list.append(news_article)
#     return news_info_list
