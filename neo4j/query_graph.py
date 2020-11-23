from database import driver, GraphDatabase

# In these queries, returning only the aggregation is easier to handle as returning anything else would result in an empty result when there is nothing to aggregate

def query_num_connections(tx, company1, company2, schema):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.{attribute1} = $company1 AND b.{attribute2} = $company2 " 
        "RETURN count(*) AS Connections"
    ).format(attribute1 = schema[0], attribute2 = schema[1])
    return tx.run(query, company1 = company1, company2 = company2).single().value()

def get_num_connections(company1, company2, schema = ['name', 'name']):
    # schema is a list of size 2 that specifies the attributes that identify the companies that are passed in (either through 'name' or 'symbol')
    # by default, it is set to identify both companies by name
    with driver.session() as session:
        return session.read_transaction(query_num_connections, company1, company2, schema)

def query_connection_list(tx, company, attribute):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(:News)<-[:MENTIONED_IN]-(b:Listing) "
        "WHERE a.{id} = $company " 
        "RETURN collect(b.symbol) AS Connections"
    ).format(id = attribute)
    return tx.run(query, company = company).single().value()

def get_list_connections(company, attribute = 'name'):
    # If company name is True, treat the parameter as a name (default), otherwise treat it as a symbol
    with driver.session() as session:
        return session.read_transaction(query_connection_list, company, attribute)

def query_url_list(tx, company, attribute):
    query = (
        "MATCH (a:Listing)-[:MENTIONED_IN]->(b:News) "
        "WHERE a.{id} = $company " 
        "RETURN collect(b.url) AS URL_List"
    ).format(id = attribute)
    return tx.run(query, company = company).single().value()

def get_url_list(company, attribute = 'name'):
    # If company name is True, treat the parameter as a name (default), otherwise treat it as a symbol
    with driver.session() as session:
        return session.read_transaction(query_url_list, company, attribute)

