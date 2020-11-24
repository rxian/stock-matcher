from relate import *

class News:
    def __init__(self, url, description, title, timestamp):
        # use URL as primary key
        self.url = url
        self.title = title
        self.description = description
        self.mentioned_companies = extract_orgs(description)
        self.timestamp = timestamp


