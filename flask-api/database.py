import os

from flaskext.mysql import MySQL
from neo4j import GraphDatabase, basic_auth

mysql = MySQL()

# NOTE: Not used yet
NEO4J_DATABASE_URL = os.environ['_NEO4J_DATABASE_URL']
NEO4J_DATABASE_USERNAME = os.environ['_NEO4J_DATABASE_USERNAME']
NEO4J_DATABASE_PASSWORD = os.environ['_NEO4J_DATABASE_PASSWORD']
driver = GraphDatabase.driver(NEO4J_DATABASE_URL, auth=basic_auth(NEO4J_DATABASE_USERNAME, str(NEO4J_DATABASE_PASSWORD)))


def connect_db():
    conn = mysql.connect()
    return conn.cursor()
