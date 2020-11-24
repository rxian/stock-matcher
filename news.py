from news_info import *

class News:
    title = ""
    description = ""
    mentioned_companies = []

    def __init__(self, url):
        # use URL as primary key
        self.url = url
        self.title = get_title(url)
        self.description = get_description(url)
        self.mentioned_companies = extract_orgs(description)

    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_mentioned_companies(self):
        return self.mentioned_companies
    
    