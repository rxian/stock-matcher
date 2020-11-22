from relate import *
from news_info import *

class News:
    def __init__(self, url, description, title, mentioned_companies):
        # use URL as primary key
        self.url = url
        self.title = get_title(url)
        self.description = get_description(url)
        self.mentioned_companies = extract_orgs(description)
