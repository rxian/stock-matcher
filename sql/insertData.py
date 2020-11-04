from connection import sqlalchemy, engine

def importPricesFromCsv(path):
    '''
    Import stock prices from a CSV file with columns (symbol,date,open,close,high,low,volume,cap) into `Prices`, and add new listings into `Listings` for symbols not found in `Listings` (or if symbol is inactive).
    '''

    with engine.connect() as conn:

        conn.execute('''
            DROP TEMPORARY TABLE IF EXISTS ImportPrices;''')

        conn.execute('''
            CREATE TEMPORARY TABLE ImportPrices(
                symbol      VARCHAR(50),
                date        DATE,
                open        REAL,
                close       REAL,
                high        REAL,
                low         REAL,
                volume      REAL,
                cap         REAL
            );''')

        conn.execute(sqlalchemy.text('''
            LOAD DATA INFILE :x
            INTO TABLE ImportPrices
            FIELDS TERMINATED BY ','
            OPTIONALLY ENCLOSED BY '"'
            LINES TERMINATED BY '\\n'
            IGNORE 1 ROWS;'''),x=path)

        conn.execute('''
            INSERT INTO Listings (symbol, active)
            SELECT s.symbol, 1
            FROM (SELECT DISTINCT symbol FROM ImportPrices) s LEFT OUTER JOIN Listings l ON s.symbol = l.symbol AND l.active = 1
            WHERE l.listingID IS NULL;''')

        conn.execute('''
            INSERT IGNORE INTO Prices
            SELECT l.listingID,p.date,p.open,p.close,p.high,p.low,p.volume,p.cap
            FROM ImportPrices p JOIN Listings l ON p.symbol = l.symbol AND l.active = 1;''')
