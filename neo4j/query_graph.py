from database import driver, GraphDatabase

# In these queries, returning only the aggregation is easier to handle as returning anything else would result in an empty result when there is nothing to aggregate

def query_num_connections(tx, company1, company2, schema):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.{attribute1} = $company1 AND b.{attribute2} = $company2 " 
        "RETURN count(*) AS Connections"
    ).format(attribute1 = schema[0], attribute2 = schema[1])
    return tx.run(query, company1 = company1, company2 = company2).single().value()

def query_num_connections_by_date(tx, company1, company2, schema, date):
    query = (
        "WITH (datetime() - duration({{years: $years, days: $days, months: $months}})) AS dateRange "
        "MATCH (a:Listing)-[:MENTIONED_IN]->(article:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.{attribute1} = $company1 AND b.{attribute2} = $company2 AND article.timestamp.epochSeconds >= dateRange.epochSeconds " 
        "RETURN count(*) AS Connections"
    ).format(attribute1 = schema[0], attribute2 = schema[1])
    return tx.run(query, years = date["years"], days = date["days"], months = date["months"], company1 = company1, company2 = company2).single().value()

def get_num_connections(company1, company2, schema = ['name', 'name'], date = None):
    # schema is a list of size 2 that specifies the attributes that identify the companies that are passed in (either through 'name' or 'symbol')
    # by default, it is set to identify both companies by name

    # date is None by defult (no date limit when querying), but if specified it is assumed to be in the format 
    # {"month": something, "date": something, "year": something} where each value in the 
    # dict is a positive integer specifying how far back to look for relationships (subject to change)
    with driver.session() as session:
        if not date:
            return session.read_transaction(query_num_connections, company1, company2, schema)
        else:
            return session.read_transaction(query_num_connections_by_date, company1, company2, schema, date)

def query_connection_list(tx, company, attribute):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.{id} = $company " 
        "RETURN collect(distinct b.symbol) AS Connections"
    ).format(id = attribute)
    return tx.run(query, company = company).single().value()

def query_connection_list_by_date(tx, company, attribute, date):
    query = (
        "WITH (datetime() - duration({{years: $years, days: $days, months: $months}})) AS dateRange "
        "MATCH (a:Listing)-[:MENTIONED_IN]->(article:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.{id} = $company AND article.timestamp.epochSeconds >= dateRange.epochSeconds "
        "RETURN collect(distinct b.symbol) AS Connections"
    ).format(id = attribute)
    return tx.run(query, years = date["years"], days = date["days"], months = date["months"], company = company).single().value()

def get_connection_list(company, attribute = 'name', date = None):
    # If company name is True, treat the parameter as a name (default), otherwise treat it as a symbol

    # date is None by defult (no date limit when querying), but if specified it is assumed to be in the format 
    # {"month": something, "date": something, "year": something} where each value in the 
    # dict is a positive integer specifying how far back to look for relationships (subject to change)
    with driver.session() as session:
        if not date:
            return session.read_transaction(query_connection_list, company, attribute)
        else:
            return session.read_transaction(query_connection_list_by_date, company, attribute, date)

def query_url_list(tx, company, attribute):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(b:News) "
        "WHERE a.{id} = $company " 
        "RETURN collect(distinct b.url) AS URL_List"
    ).format(id = attribute)
    return tx.run(query, company = company).single().value()

def query_url_list_by_date(tx, company, attribute, date):
    query = (
        "WITH (datetime() - duration({{years: $years, days: $days, months: $months}})) AS dateRange "
        "MATCH (a:Listing)-[:MENTIONED_IN]->(b:News) "
        "WHERE a.{id} = $company AND b.timestamp.epochSeconds >= dateRange.epochSeconds "
        "RETURN collect(distinct b.url) AS URL_List"
    ).format(id = attribute)
    return tx.run(query, years = date["years"], days = date["days"], months = date["months"], company = company).single().value()

def get_url_list(company, attribute = 'name', date = None):
    # If company name is True, treat the parameter as a name (default), otherwise treat it as a symbol

    # date is None by defult (no date limit when querying), but if specified it is assumed to be in the format 
    # {"month": something, "date": something, "year": something} where each value in the 
    # dict is a positive integer specifying how far back to look for relationships (subject to change)
    with driver.session() as session:
        if not date:
            return session.read_transaction(query_url_list, company, attribute)
        else:
            return session.read_transaction(query_url_list_by_date, company, attribute, date)

