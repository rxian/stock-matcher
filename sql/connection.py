import sqlalchemy
import os.path

host = 'mysql+pymysql://root@localhost:33003'
database = 'stock_matcher'
options = 'charset=utf8mb4'

engine = sqlalchemy.create_engine(os.path.join(host,database)+'?'+options)
