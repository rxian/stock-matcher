class News:
    title = ""
    description = ""
    mentioned_companies = []
    timestamp = ""

    def __init__(self, url, description, mentioned_companies, title, timestamp):
        # use URL as primary key
        self.url = url
        self.title = title
        self.description = description
        self.mentioned_companies = mentioned_companies
        self.timestamp = timestamp

    def get_title(self) -> str:
        return self.title

    def get_description(self) -> str:
        return self.description

    def get_mentioned_companies(self) -> list:
        return self.mentioned_companies

    def get_timestamp(self) -> str:
        return self.timestamp

