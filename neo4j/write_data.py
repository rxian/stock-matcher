from database import driver, GraphDatabase

def create_listing(tx, listing_id: int, listing_name: str, listing_symbol: str, listing_industry: str, listing_sector: str, listing_market_cap: int):
    tx.run("MERGE (a:Listing {listing_id: $listing_id, name: $listing_name, symbol: $listing_symbol, industry: $listing_industry, sector: $listing_sector, market_cap: $listing_market_cap})", listing_id = listing_id, listing_name = listing_name, listing_symbol = listing_symbol, listing_industry = listing_industry, listing_sector = listing_sector, listing_market_cap = listing_market_cap)

def insert_listings(ticker_company_name_dict: dict):
    with driver.session() as session:
        for listing_id in ticker_company_name_dict.keys():
            session.write_transaction(create_listing, int(listing_id), ticker_company_name_dict[listing_id]["name"], ticker_company_name_dict[listing_id]["symbol"], ticker_company_name_dict[listing_id]["industry"], ticker_company_name_dict[listing_id]["sector"], ticker_company_name_dict[listing_id]["sector"], ticker_company_name_dict[listing_id]["market_cap"])

def create_news(tx, url: str, title: str, company: str, timestamp: str):
    query = (
        "MERGE (article:News {title: $title, url: $url, timestamp: datetime($timestamp)}) "
        "WITH article "
        "MATCH (a:Listing {symbol: $company}) "
        "MERGE (a)-[:MENTIONED_IN]->(article)"
    )
    tx.run(query, title = title, url = url, company = company, timestamp = timestamp)

def insert_news(articles: list):
    with driver.session() as session:
        for article in articles:
            for company in article.mentioned_companies:
                session.write_transaction(create_news, article.url, article.title, company, article.timestamp)

def update_listing(tx, company: int, attribute: str, value):
    query = (
        "MATCH (a:Listing) "
        "WHERE a.listing_id = $company "
        "SET a.{attr} = $value"
    ).format(attr = attribute)
    tx.run(query, company = company, value = value)

def update_listing_attribute(company: int, attribute: str, value):
    with driver.session() as session:
        session.write_transaction(update_listing, company, attribute, value)

def delete_listing(tx, company: int):
    query = (
        "MATCH (a:Listing) "
        "WHERE a.listing_id = $company "
        "DETACH DELETE a"
    )
    tx.run(query, company = company)

def remove_listing(company: int):
    with driver.session() as session:
        session.write_transaction(delete_listing, company)

def delete_news_by_age(tx, age: dict):
    query = (
        "WITH (datetime() - duration({years: $years, days: $days, months: $months})) AS dateRange "
        "MATCH (article:News) "
        "WHERE article.timestamp.epochSeconds < dateRange.epochSeconds "
        "DETACH DELETE article"
    )
    tx.run(query, years = age["years"], days = age["days"], months = age["months"])

def remove_news_by_age(age: dict):
    # age is in the format {"months": something, "days": something, "years": something}, which specifies how far back to go from the current date
    # articles that are less than the specified age are untouched while those that are older than the specified age are deleted
    with driver.session() as session:
        session.write_transaction(delete_news_by_age, age)

def delete_news_by_url(tx, url: str):
    query = (
        "MATCH (article:News) "
        "WHERE article.url = $url "
        "DETACH DELETE article"
    )
    tx.run(query, url = url)

def remove_news_by_url(url: str):
    with driver.session() as session:
        session.write_transaction(delete_news_by_url, url)

# pull news from here: https://www.nasdaq.com/feed/rssoutbound?symbol={REPLACE_WITH_STOCK_SYMBOL} or https://feeds.finance.yahoo.com/rss/2.0/headline?s={REPLACE_WITH_STOCK_SYMBOL}&region=US&lang=en-US
# currently only pulling from nasdaq.com's rss feed