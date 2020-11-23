from database import driver, GraphDatabase

# In these queries, returning only the aggregation is easier to handle as returning anything else would result in an empty result when there is nothing to aggregate

def query_num_conn_by_symbol(tx, company1, company2):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.symbol = $company1 AND b.symbol = $company2 " 
        "RETURN count(*) AS Connections"
    )
    return tx.run(query, company1 = company1, company2 = company2).single().value()

def query_num_conn_by_name(tx, company1, company2):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.name = $company1 AND b.name = $company2 " 
        "RETURN count(*) AS Connections"
    )
    return tx.run(query, company1 = company1, company2 = company2).single().value()

def get_num_connections(company1, company2, company_name = True):
    # If company name is True, treat both parameters as names (default), otherwise treat them as symbols
    with driver.session() as session:
        if company_name:
            return session.read_transaction(query_num_conn_by_name, company1, company2)
        else:
            return session.read_transaction(query_num_conn_by_symbol, company1, company2)

def query_list_conn_by_symbol(tx, company):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.symbol = $company " 
        "RETURN collect(b.symbol) AS Connections"
    )
    return tx.run(query, company = company).single().value()

def query_list_conn_by_name(tx, company):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.name = $company " 
        "RETURN collect(b.symbol) AS Connections"
    )
    return tx.run(query, company = company).single().value()

def get_list_connections(company, company_name = True):
    # If company name is True, treat the parameter as a name (default), otherwise treat it as a symbol
    with driver.session() as session:
        if company_name:
            return session.read_transaction(query_list_conn_by_name, company)
        else:
            return session.read_transaction(query_list_conn_by_symbol, company)

def query_url_list_by_symbol(tx, company):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(b:News) "
        "WHERE a.symbol = $company " 
        "RETURN collect(b.url) AS URL_List"
    )
    return tx.run(query, company = company).single().value()

def query_url_list_by_name(tx, company):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(b:News) "
        "WHERE a.name = $company " 
        "RETURN collect(b.url) AS URL_List"
    )
    return tx.run(query, company = company).single().value()

def get_url_list(company, company_name = True):
    # If company name is True, treat the parameter as a name (default), otherwise treat it as a symbol
    with driver.session() as session:
        if company_name:
            return session.read_transaction(query_url_list_by_name, company)
        else:
            return session.read_transaction(query_url_list_by_symbol, company)

