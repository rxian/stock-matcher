from database import driver, GraphDatabase

def create_listing(tx, listing_id: int, listing_name: str, listing_symbol: str):
    tx.run("MERGE (a:Listing {listing_id: $listing_id, name: $listing_name, symbol: $listing_symbol})", listing_id = listing_id, listing_name = listing_name, listing_symbol = listing_symbol)

def insert_listings(ticker_company_name_dict: dict):
    with driver.session() as session:
        listing_id = 0
        for symbol in ticker_company_name_dict.keys():
            session.write_transaction(create_listing, listing_id, ticker_company_name_dict[symbol], symbol)
            listing_id += 1

def create_news(tx, url: str, title: str, company: str, timestamp: str):
    query = (
        "MERGE (article:News {title: $title, url: $url, timestamp: datetime($timestamp)}) "
        "WITH article "
        "MATCH (a:Listing {name: $company}) "
        "MERGE (a)-[:MENTIONED_IN]->(article)"
    )
    tx.run(query, title = title, url = url, company = company, timestamp = timestamp)

def insert_news(articles: list):
    with driver.session() as session:
        for article in articles:
            for company in article.mentioned_companies:
                session.write_transaction(create_news, article.url, article.title, company, article.timestamp)

# pull news from here: https://www.nasdaq.com/feed/rssoutbound?symbol={REPLACE_WITH_STOCK_SYMBOL} and https://feeds.finance.yahoo.com/rss/2.0/headline?s={REPLACE_WITH_STOCK_SYMBOL}&region=US&lang=en-US