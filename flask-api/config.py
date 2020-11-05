import os


class Development(object):
    MYSQL_DATABASE_HOST = os.environ['_MYSQL_DATABASE_HOST']
    MYSQL_DATABASE_PORT = int(os.environ['_MYSQL_DATABASE_PORT'])
    MYSQL_DATABASE_DB = os.environ['_MYSQL_DATABASE_DB']
    MYSQL_DATABASE_USER = os.environ['_MYSQL_DATABASE_USER']
    MYSQL_DATABASE_PASSWORD = os.environ['_MYSQL_DATABASE_PASSWORD']


app_config = {
    'development': Development
}