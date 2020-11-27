# from database import driver, GraphDatabase
from typing import Optional

from database import driver


def query_num_connections(tx, company1: int, company2: int, date: Optional[dict] = None) -> int:
    date_comparison = "AND article.timestamp.epochSeconds >= dateRange.epochSeconds "
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(article:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.listing_id = $company1 AND b.listing_id = $company2 {date_compare}"
        "RETURN count(*) AS Connections"
    ).format(date_compare = "" if not date else date_comparison)
    if not date:
        return tx.run(query, company1 = company1, company2 = company2).single().value()
    else:
        date_min = "WITH (datetime() - duration({years: $years, days: $days, months: $months})) AS dateRange "
        return tx.run(date_min + query, years = date["years"], days = date["days"], months = date["months"], company1 = company1, company2 = company2).single().value()

def get_num_connections(company1: int, company2: int, date: Optional[dict] = None) -> int:
    # date is None by defult (no date limit when querying), but if specified it is assumed to be in the format
    # {"months": something, "days": something, "years": something} where each value in the
    # dict is a positive integer specifying how far back to look for relationships (subject to change)
    with driver.session() as session:
        return session.read_transaction(query_num_connections, company1, company2, date)

def query_connection_list(tx, company: int, limit: Optional[int] = None, date: Optional[dict] = None) -> list:
    date_comparison = "AND article.timestamp.epochSeconds >= dateRange.epochSeconds "
    limit_query = " LIMIT $n"
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(article:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.listing_id = $company {date_compare}"
        "RETURN b.listing_id AS Listing_Id, b.symbol AS Symbol, count(distinct article.url) AS Connections "
        "ORDER BY Connections DESC, b.listing_id{limit_query}"
    ).format(date_compare = "" if not date else date_comparison, limit_query = "" if not limit else limit_query)
    if not date:
        return list(tx.run(query, {"company": company, "n": limit}))
    else:
        date_min = "WITH (datetime() - duration({years: $years, days: $days, months: $months})) AS dateRange "
        return tx.run(date_min + query, years = date["years"], days = date["days"], months = date["months"], company = company, n = limit).values()

def get_connection_list(company: int, limit: Optional[int] = None, date: Optional[dict] = None) -> list:
    # date is None by defult (no date limit when querying), but if specified it is assumed to be in the format
    # {"months": something, "days": something, "years": something} where each value in the
    # dict is a positive integer specifying how far back to look for relationships (subject to change)
    with driver.session() as session:
        result = session.read_transaction(query_connection_list, company, limit, date)
        return [dict(zip(r.keys(), r.values())) for r in result]

def query_article_list(tx, company: int, limit: Optional[int] = None, date: Optional[dict] = None) -> list:
    date_comparison = "AND article.timestamp.epochSeconds >= dateRange.epochSeconds "
    limit_query = " LIMIT $n"
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(article:News) "
        "WHERE a.listing_id = $company {date_compare}"
        "RETURN article.title AS Title, article.url AS URL "
        "ORDER BY article.timestamp.epochSeconds DESC{limit_query}"
    ).format(date_compare = "" if not date else date_comparison, limit_query = "" if not limit else limit_query)
    if not date:
        return list(tx.run(query, {"company": company, "n": limit}))
    else:
        date_min = "WITH (datetime() - duration({years: $years, days: $days, months: $months})) AS dateRange "
        return tx.run(date_min + query, years = date["years"], days = date["days"], months = date["months"], company = company, n = limit).values()


def get_article_list(company: int, limit: Optional[int] = None, date: Optional[dict] = None) -> list:
    # date is None by defult (no date limit when querying), but if specified it is assumed to be in the format
    # {"months": something, "days": something, "years": something} where each value in the
    # dict is a positive integer specifying how far back to look for relationships (subject to change)
    with driver.session() as session:
        result = session.read_transaction(query_article_list, company, limit, date)
        return [dict(zip(r.keys(), r.values())) for r in result]

def query_similar_companies(tx, company: int, attribute: str, limit: Optional[int] = None) -> list:
    limit_query = " LIMIT $n"
    query = (
        "MATCH (a:Listing), (b:Listing) "
        "WHERE a.listing_id = $company AND a.{attr} = b.{attr} AND a.listing_id <> b.listing_id "
        "RETURN b.listing_id AS Listing_Id, b.symbol AS Symbol "
        "ORDER BY Listing_Id{limit_query}"
    ).format(attr = attribute, limit_query = "" if not limit else limit_query)
    return tx.run(query, company = company, n = limit).values()

def get_similar_companies(company: int, attribute: str = "sector", limit: Optional[int] = None) -> list:
    # attribute can either be "sector" or "industry"; the default is "sector"
    with driver.session() as session:
        return session.read_transaction(query_similar_companies, company, attribute, limit)

def query_industry_sector_total_companies(tx, attribute: str, limit: Optional[int] = None) -> list:
    limit_query = " LIMIT $n"
    query = (
        "MATCH (a:Listing) "
        "RETURN a.{attr} AS {attr}, count(distinct a) AS Total "
        "ORDER BY Total DESC{limit_query}"
    ).format(attr = attribute, limit_query = "" if not limit else limit_query)
    return tx.run(query, n = limit).values()

def get_industry_sector_total_companies(attribute: str = "sector", limit: Optional[int] = None) -> list:
    # attribute can either be "sector" or "industry"; the default is "sector"
    with driver.session() as session:
        return session.read_transaction(query_industry_sector_total_companies, attribute, limit)

def query_industry_sector_total_market_cap(tx, attribute: str, limit: Optional[int] = None) -> list:
    limit_query = " LIMIT $n"
    query = (
        "MATCH (a:Listing) "
        "RETURN a.{attr} AS {attr}, sum(a.market_cap) AS Total "
        "ORDER BY Total DESC{limit_query}"
    ).format(attr = attribute, limit_query = "" if not limit else limit_query)
    return tx.run(query, n = limit).values()

def get_industry_sector_total_market_cap(attribute: str = "sector", limit: Optional[int] = None) -> list:
    # attribute can either be "sector" or "industry"; the default is "sector"
    with driver.session() as session:
        return session.read_transaction(query_industry_sector_total_market_cap, attribute, limit)

