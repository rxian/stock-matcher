from database import driver, GraphDatabase
from generate_sp_500_list import ticker_company_name_dict

def create_listing(tx, listing_id, listing_name, listing_symbol):
    tx.run("MERGE (a:Listing {listing_id: $listing_id, name: $listing_name, symbol: $listing_symbol})", listing_id = listing_id, listing_name = listing_name, listing_symbol = listing_symbol)
    return

def insert_listings():
    with driver.session() as session:
        listing_id = 0
        for symbol in ticker_company_name_dict.keys():
            session.write_transaction(create_listing, listing_id, ticker_company_name_dict[symbol], symbol)
            listing_id += 1
        return

def create_news(tx, url, title, company, timestamp):
    query = (
        "MERGE (article:News {title: $title, url: $url, timestamp: datetime($timestamp)}) "
        "WITH article "
        "MATCH (a:Listing {name: $company}) "
        "MERGE (a)-[:MENTIONED_IN]->(article)"
    )
    tx.run(query, title = title, url = url, company = company, timestamp = timestamp)
    return

def insert_news(articles):
    with driver.session() as session:
        for article in articles:
            for company in article.mentioned_companies:
                session.write_transaction(create_news, article.url, article.title, company, article.timestamp)
        return

